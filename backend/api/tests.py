import json
from datetime import date, timedelta, time
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from .models import (
    Destination, TourPackage, Hotel, RoomType,
    SeasonalPricing, GuideProfile, TourSlot, Booking,
    PaymentTransaction, PaymentWebhookLog, Invoice
)

User = get_user_model()


class AuthAndRBACApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.traveller = User.objects.create_user(
            email='traveller@voyagecraft.com',
            password='TestPassword123!',
            full_name='Test Traveller',
            role='TRAVELLER'
        )
        self.admin_user = User.objects.create_superuser(
            email='admin@voyagecraft.com',
            password='AdminPassword123!',
            full_name='Platform Admin'
        )

    def test_user_registration(self):
        response = self.client.post('/api/auth/register/', {
            'email': 'newtraveller@voyagecraft.com',
            'password': 'SecurePassword88!',
            'password_confirm': 'SecurePassword88!',
            'full_name': 'New Explorer',
            'role': 'TRAVELLER',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], 'newtraveller@voyagecraft.com')

    def test_jwt_login(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'traveller@voyagecraft.com',
            'password': 'TestPassword123!',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['role'], 'TRAVELLER')

    def test_user_profile_authenticated(self):
        self.client.force_authenticate(user=self.traveller)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'traveller@voyagecraft.com')
        self.assertEqual(response.data['full_name'], 'Test Traveller')

    def test_rbac_admin_analytics_forbidden_for_traveller(self):
        self.client.force_authenticate(user=self.traveller)
        response = self.client.get('/api/admin/analytics/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rbac_admin_analytics_allowed_for_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/admin/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_revenue', response.data)


class HotelAndGuideEngineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.destination = Destination.objects.create(
            name='Santorini',
            country='Greece',
            region='Europe',
            description='Sun-drenched caldera cliffside luxury.',
            image_url='https://example.com/santorini.jpg'
        )
        self.hotel = Hotel.objects.create(
            destination=self.destination,
            name='Canaves Oia Suites',
            slug='canaves-oia-suites',
            address='Oia, Santorini 847 02, Greece',
            star_rating=5,
            description='Luxury cliffside cave suites with private plunge pools.',
            image_url='https://example.com/hotel.jpg',
            amenities=['Infinity Pool', 'Private Butler', 'Fine Dining']
        )
        self.room = RoomType.objects.create(
            hotel=self.hotel,
            name='Infinity Caldera Suite',
            slug='infinity-caldera-suite',
            max_occupancy=2,
            base_price_per_night=Decimal('500.00'),
            total_rooms=5
        )
        self.guide_user = User.objects.create_user(
            email='guide@voyagecraft.com',
            password='GuidePassword123!',
            full_name='Elena Vassiliou',
            role='GUIDE'
        )
        self.guide = GuideProfile.objects.create(
            user=self.guide_user,
            bio='Expert local historian and volcanic geologist.',
            spoken_languages=['English', 'Greek', 'French'],
            experience_years=8,
            rating=4.95,
            is_verified=True
        )
        self.tour = TourPackage.objects.create(
            destination=self.destination,
            title='Caldera Sunset Catamaran & Volcanic Springs',
            slug='caldera-sunset-catamaran',
            category='Luxury',
            price_per_person=Decimal('250.00'),
            group_size_max=12
        )

    def test_hotel_listing_api(self):
        response = self.client.get('/api/hotels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Canaves Oia Suites')
        self.assertEqual(response.data[0]['destination_name'], 'Santorini')

    def test_room_availability_quote_and_seasonal_pricing(self):
        start = date.today() + timedelta(days=10)
        end = start + timedelta(days=3)

        SeasonalPricing.objects.create(
            room_type=self.room,
            name='Weekend Peak Rush',
            start_date=start + timedelta(days=1),
            end_date=start + timedelta(days=1),
            price_multiplier=Decimal('1.50')
        )

        url = f"/api/hotels/{self.hotel.id}/rooms/{self.room.id}/availability/?start_date={start.isoformat()}&end_date={end.isoformat()}&rooms=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_available'])
        self.assertEqual(response.data['nights_count'], 3)
        self.assertEqual(response.data['total_price'], 1750.0)

    def test_hotel_booking_creation(self):
        start = date.today() + timedelta(days=5)
        end = start + timedelta(days=2)

        payload = {
            'booking_type': 'HOTEL',
            'room_type': self.room.id,
            'check_in_date': start.isoformat(),
            'check_out_date': end.isoformat(),
            'rooms_count': 1,
            'customer_name': 'Alexander Wright',
            'customer_email': 'alex@example.com',
            'customer_phone': '+1234567890',
            'guests_count': 2,
        }
        response = self.client.post('/api/bookings/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['total_price']), 1000.0)
        self.assertEqual(response.data['status'], 'CONFIRMED')
        self.assertTrue(response.data['booking_reference'].startswith('TRV-'))

    def test_tour_slot_creation_and_booking_capacity_decrement(self):
        slot_date = date.today() + timedelta(days=7)
        slot = TourSlot.objects.create(
            tour=self.tour,
            guide=self.guide,
            slot_date=slot_date,
            start_time=time(9, 30),
            max_capacity=10,
            booked_count=0
        )
        self.assertEqual(slot.remaining_capacity, 10)

        payload = {
            'booking_type': 'ACTIVITY',
            'tour_slot': slot.id,
            'customer_name': 'Sarah Connor',
            'customer_email': 'sarah@example.com',
            'customer_phone': '+1987654321',
            'guests_count': 4,
        }
        response = self.client.post('/api/bookings/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        slot.refresh_from_db()
        self.assertEqual(slot.booked_count, 4)
        self.assertEqual(slot.remaining_capacity, 6)


class ConcurrencyAndPaymentEngineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.destination = Destination.objects.create(
            name='Kyoto',
            country='Japan',
            region='Asia',
            description='Ancient bamboo groves and imperial temples.',
            image_url='https://example.com/kyoto.jpg'
        )
        self.tour = TourPackage.objects.create(
            destination=self.destination,
            title='Kyoto Zen Sanctuaries & Tea Ceremony',
            slug='kyoto-zen-sanctuaries',
            category='Cultural',
            price_per_person=Decimal('150.00'),
            group_size_max=10
        )
        self.slot = TourSlot.objects.create(
            tour=self.tour,
            slot_date=date.today() + timedelta(days=15),
            start_time=time(10, 0),
            max_capacity=2,  # Only 2 seats for testing concurrency limits
            booked_count=0
        )

    def test_booking_temporary_hold(self):
        # Place a 10-minute hold for 1 seat
        payload = {
            'booking_type': 'ACTIVITY',
            'tour_slot': self.slot.id,
            'customer_name': 'Kenji Sato',
            'customer_email': 'kenji@example.com',
            'customer_phone': '+819012345678',
            'guests_count': 1,
        }
        response = self.client.post('/api/bookings/hold/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'PENDING_HOLD')
        self.assertEqual(response.data['hold_seconds_remaining'], 600)
        self.assertIn('booking_reference', response.data)

        # Check slot remaining capacity decremented to 1
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.remaining_capacity, 1)

    def test_double_booking_prevention_on_exhausted_slot(self):
        # User 1 reserves the only 2 available seats
        payload1 = {
            'booking_type': 'ACTIVITY',
            'tour_slot': self.slot.id,
            'customer_name': 'First Traveller',
            'customer_email': 'first@example.com',
            'customer_phone': '+1111111111',
            'guests_count': 2,
        }
        res1 = self.client.post('/api/bookings/hold/', payload1, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # User 2 attempts to reserve 1 seat at the same time
        payload2 = {
            'booking_type': 'ACTIVITY',
            'tour_slot': self.slot.id,
            'customer_name': 'Second Traveller',
            'customer_email': 'second@example.com',
            'customer_phone': '+2222222222',
            'guests_count': 1,
        }
        res2 = self.client.post('/api/bookings/hold/', payload2, format='json')
        # Double booking prevented!
        self.assertEqual(res2.status_code, status.HTTP_409_CONFLICT)
        self.assertIn('error', res2.data)

    def test_payment_order_creation_stripe_and_razorpay(self):
        # Create a booking on hold
        booking = Booking.objects.create(
            tour=self.tour,
            booking_type='TOUR',
            customer_name='Marcus Aurelius',
            customer_email='marcus@example.com',
            customer_phone='+3906123456',
            departure_date=date.today() + timedelta(days=20),
            guests_count=2,
            price_per_person=Decimal('150.00'),
            total_price=Decimal('300.00'),
            status='PENDING_HOLD',
            hold_expires_at=timezone.now() + timedelta(minutes=10)
        )

        # 1. Stripe order creation
        stripe_res = self.client.post('/api/payments/create-order/', {
            'booking_reference': booking.booking_reference,
            'provider': 'STRIPE'
        })
        self.assertEqual(stripe_res.status_code, status.HTTP_200_OK)
        self.assertEqual(stripe_res.data['provider'], 'STRIPE')
        self.assertIn('client_secret', stripe_res.data)

        # 2. Razorpay order creation
        rzp_res = self.client.post('/api/payments/create-order/', {
            'booking_reference': booking.booking_reference,
            'provider': 'RAZORPAY'
        })
        self.assertEqual(rzp_res.status_code, status.HTTP_200_OK)
        self.assertEqual(rzp_res.data['provider'], 'RAZORPAY')
        self.assertEqual(rzp_res.data['currency'], 'INR')

    def test_stripe_webhook_confirms_booking_idempotently(self):
        booking = Booking.objects.create(
            tour=self.tour,
            booking_type='TOUR',
            customer_name='Helena Troy',
            customer_email='helena@example.com',
            customer_phone='+3021012345',
            departure_date=date.today() + timedelta(days=30),
            guests_count=1,
            price_per_person=Decimal('150.00'),
            total_price=Decimal('150.00'),
            status='PENDING_HOLD',
            hold_expires_at=timezone.now() + timedelta(minutes=10)
        )

        event_payload = {
            'id': 'evt_test_12345_unique',
            'type': 'payment_intent.succeeded',
            'data': {
                'object': {
                    'id': 'pi_test_charge_999',
                    'metadata': {
                        'booking_reference': booking.booking_reference
                    }
                }
            }
        }

        # First webhook call
        response = self.client.post(
            '/api/payments/webhook/stripe/',
            data=json.dumps(event_payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_valid_stripe_signature'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        booking.refresh_from_db()
        self.assertEqual(booking.status, 'CONFIRMED')
        self.assertTrue(hasattr(booking, 'invoice'))
        self.assertTrue(booking.invoice.is_paid)

        # Second webhook call with same event_id (idempotency guard)
        response_dup = self.client.post(
            '/api/payments/webhook/stripe/',
            data=json.dumps(event_payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_valid_stripe_signature'
        )
        self.assertEqual(response_dup.status_code, status.HTTP_200_OK)
        self.assertEqual(response_dup.data['message'], 'Webhook already processed.')

    def test_cancellation_tiered_refund_policy(self):
        # Case A: > 14 days before start -> 100% refund
        booking_far = Booking.objects.create(
            tour=self.tour,
            customer_name='Far Traveller',
            customer_email='far@example.com',
            departure_date=date.today() + timedelta(days=25),
            total_price=Decimal('500.00'),
            status='CONFIRMED'
        )
        res_far = self.client.post(f"/api/bookings/{booking_far.booking_reference}/cancel/", {'reason': 'Schedule change'})
        self.assertEqual(res_far.status_code, status.HTTP_200_OK)
        self.assertEqual(res_far.data['refund_amount'], 500.0)
        self.assertEqual(res_far.data['status'], 'REFUNDED')

        # Case B: 10 days before start (7-14 range) -> 50% refund
        booking_mid = Booking.objects.create(
            tour=self.tour,
            customer_name='Mid Traveller',
            customer_email='mid@example.com',
            departure_date=date.today() + timedelta(days=10),
            total_price=Decimal('400.00'),
            status='CONFIRMED'
        )
        res_mid = self.client.post(f"/api/bookings/{booking_mid.booking_reference}/cancel/")
        self.assertEqual(res_mid.status_code, status.HTTP_200_OK)
        self.assertEqual(res_mid.data['refund_amount'], 200.0)
        self.assertEqual(res_mid.data['status'], 'REFUNDED')

        # Case C: 2 days before start (< 7 days) -> 0% refund (Non-refundable)
        booking_close = Booking.objects.create(
            tour=self.tour,
            customer_name='Close Traveller',
            customer_email='close@example.com',
            departure_date=date.today() + timedelta(days=2),
            total_price=Decimal('300.00'),
            status='CONFIRMED'
        )
        res_close = self.client.post(f"/api/bookings/{booking_close.booking_reference}/cancel/")
        self.assertEqual(res_close.status_code, status.HTTP_200_OK)
        self.assertEqual(res_close.data['refund_amount'], 0.0)
        self.assertEqual(res_close.data['status'], 'CANCELLED')
