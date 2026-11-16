from datetime import date, timedelta, time
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import (
    Destination, TourPackage, Hotel, RoomType,
    SeasonalPricing, GuideProfile, TourSlot, Booking
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
        end = start + timedelta(days=3)  # 3 nights

        # Add a seasonal surge (1.5x) for the middle night
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
        # Night 1: 500, Night 2: 750 (500 * 1.5), Night 3: 500 => Total = 1750
        self.assertEqual(response.data['total_price'], 1750.0)

    def test_hotel_booking_creation(self):
        start = date.today() + timedelta(days=5)
        end = start + timedelta(days=2)  # 2 nights x 500 = 1000

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

        # Book 4 guests for this slot
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

        # Verify booked_count updated
        slot.refresh_from_db()
        self.assertEqual(slot.booked_count, 4)
        self.assertEqual(slot.remaining_capacity, 6)
