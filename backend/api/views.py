import json
import urllib.request
import uuid
from datetime import date, timedelta
from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q, Avg, Sum, Count, Min
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import (
    Destination, TourPackage, Hotel, RoomType,
    SeasonalPricing, RoomInventory, GuideProfile, TourSlot,
    Booking, PaymentTransaction, PaymentWebhookLog, Invoice, Review
)
from .permissions import IsAdminRole, IsVendorRole, IsGuideRole, IsOwnerOrAdmin
from .gateways import get_payment_gateway
from .invoice_utils import generate_booking_invoice
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserProfileSerializer,
    GoogleAuthSerializer,
    DestinationSerializer,
    TourPackageListSerializer,
    TourPackageDetailSerializer,
    HotelListSerializer,
    HotelDetailSerializer,
    RoomTypeSerializer,
    GuideProfileSerializer,
    TourSlotSerializer,
    BookingSerializer,
    PaymentTransactionSerializer,
    InvoiceSerializer,
    ReviewSerializer
)

User = get_user_model()


# ----------------------------------------------------
# Authentication & User Management Views
# ----------------------------------------------------

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        refresh['full_name'] = user.full_name
        refresh['role'] = user.role
        refresh['is_verified'] = user.is_verified

        return Response({
            'message': 'Account registered successfully.',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role,
                'phone_number': user.phone_number,
                'is_verified': user.is_verified,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class GoogleAuthAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        credential = serializer.validated_data['credential']
        role = serializer.validated_data.get('role', 'TRAVELLER')

        try:
            url = f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}"
            req = urllib.request.Request(url, headers={'User-Agent': 'VoyageCraft-Auth'})
            with urllib.request.urlopen(req, timeout=5) as response:
                payload = json.loads(response.read().decode())

            email = payload.get('email')
            if not email:
                return Response({'error': 'Google token does not contain email.'}, status=status.HTTP_400_BAD_REQUEST)

            full_name = payload.get('name', '')
            avatar_url = payload.get('picture', '')
            google_id = payload.get('sub')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'full_name': full_name,
                    'avatar_url': avatar_url,
                    'google_id': google_id,
                    'role': role,
                    'is_verified': True,
                }
            )

            if not created:
                updated = False
                if avatar_url and not user.avatar_url:
                    user.avatar_url = avatar_url
                    updated = True
                if google_id and not user.google_id:
                    user.google_id = google_id
                    updated = True
                if updated:
                    user.save()

            refresh = RefreshToken.for_user(user)
            refresh['email'] = user.email
            refresh['full_name'] = user.full_name
            refresh['role'] = user.role
            refresh['is_verified'] = user.is_verified
            refresh['avatar_url'] = user.avatar_url

            return Response({
                'message': 'Authenticated with Google successfully.',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'role': user.role,
                    'avatar_url': user.avatar_url,
                    'is_verified': user.is_verified,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Failed to verify Google credential: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------
# Tourist Destinations & Tour Packages Views
# ----------------------------------------------------

class DestinationListAPIView(generics.ListAPIView):
    queryset = Destination.objects.all().order_by('name')
    serializer_class = DestinationSerializer


class TourPackageListAPIView(generics.ListAPIView):
    serializer_class = TourPackageListSerializer

    def get_queryset(self):
        queryset = TourPackage.objects.select_related('destination').all()
        
        search = self.request.query_params.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(destination__name__icontains=search) |
                Q(destination__country__icontains=search) |
                Q(destination__region__icontains=search) |
                Q(short_description__icontains=search)
            )

        destination_id = self.request.query_params.get('destination')
        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)

        region = self.request.query_params.get('region')
        if region and region != 'All':
            queryset = queryset.filter(destination__region__iexact=region)

        category = self.request.query_params.get('category')
        if category and category != 'All':
            queryset = queryset.filter(category__iexact=category)

        difficulty = self.request.query_params.get('difficulty')
        if difficulty and difficulty != 'All':
            queryset = queryset.filter(difficulty__iexact=difficulty)

        min_price = self.request.query_params.get('min_price')
        if min_price:
            try:
                queryset = queryset.filter(price_per_person__gte=float(min_price))
            except ValueError:
                pass

        max_price = self.request.query_params.get('max_price')
        if max_price:
            try:
                queryset = queryset.filter(price_per_person__lte=float(max_price))
            except ValueError:
                pass

        featured = self.request.query_params.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)

        trending = self.request.query_params.get('trending')
        if trending == 'true':
            queryset = queryset.filter(is_trending=True)

        sort = self.request.query_params.get('sort', 'featured')
        if sort == 'price_low':
            queryset = queryset.order_by('price_per_person')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price_per_person')
        elif sort == 'rating':
            queryset = queryset.order_by('-rating')
        elif sort == 'duration_short':
            queryset = queryset.order_by('duration_days')
        elif sort == 'duration_long':
            queryset = queryset.order_by('-duration_days')
        else:
            queryset = queryset.order_by('-is_featured', '-rating', 'id')

        return queryset


class TourPackageDetailAPIView(generics.RetrieveAPIView):
    queryset = TourPackage.objects.select_related('destination').prefetch_related('reviews').all()
    serializer_class = TourPackageDetailSerializer
    lookup_field = 'id'


# ----------------------------------------------------
# Hotels & Accommodations Module Views
# ----------------------------------------------------

class HotelListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = HotelListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsVendorRole()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Hotel.objects.select_related('destination').prefetch_related('room_types').annotate(
            min_price_annotated=Min('room_types__base_price_per_night')
        ).all()

        search = self.request.query_params.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(destination__name__icontains=search) |
                Q(destination__country__icontains=search) |
                Q(address__icontains=search)
            )

        destination_id = self.request.query_params.get('destination')
        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)

        region = self.request.query_params.get('region')
        if region and region != 'All':
            queryset = queryset.filter(destination__region__iexact=region)

        star_rating = self.request.query_params.get('star_rating')
        if star_rating:
            try:
                queryset = queryset.filter(star_rating__gte=int(star_rating))
            except ValueError:
                pass

        featured = self.request.query_params.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)

        return queryset.order_by('-is_featured', '-star_rating', 'id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotel.objects.select_related('destination').prefetch_related('room_types__seasonal_prices', 'reviews').all()
    serializer_class = HotelDetailSerializer
    lookup_field = 'id'


class RoomAvailabilityQuoteAPIView(APIView):
    def get(self, request, hotel_id, room_id):
        try:
            room = RoomType.objects.get(id=room_id, hotel_id=hotel_id)
        except RoomType.DoesNotExist:
            return Response({'error': 'Room type not found for this hotel.'}, status=status.HTTP_404_NOT_FOUND)

        start_str = request.query_params.get('start_date')
        end_str = request.query_params.get('end_date')
        requested_rooms = int(request.query_params.get('rooms', 1))

        if not start_str or not end_str:
            return Response({'error': 'Both start_date and end_date query parameters are required (YYYY-MM-DD).'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = date.fromisoformat(start_str)
            end_date = date.fromisoformat(end_str)
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        quote = room.calculate_stay_quote(start_date, end_date, requested_rooms)
        return Response(quote, status=status.HTTP_200_OK)


# ----------------------------------------------------
# Tour Guides & Activities Views
# ----------------------------------------------------

class GuideListAPIView(generics.ListAPIView):
    serializer_class = GuideProfileSerializer

    def get_queryset(self):
        queryset = GuideProfile.objects.select_related('user').prefetch_related('destinations').filter(is_verified=True)
        destination_id = self.request.query_params.get('destination')
        if destination_id:
            queryset = queryset.filter(destinations__id=destination_id)
        return queryset.order_by('-rating', '-experience_years')


class GuideDetailAPIView(generics.RetrieveAPIView):
    queryset = GuideProfile.objects.select_related('user').prefetch_related('destinations', 'slots').all()
    serializer_class = GuideProfileSerializer
    lookup_field = 'id'


class TourSlotListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TourSlotSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsGuideRole()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = TourSlot.objects.select_related('tour', 'guide', 'guide__user').filter(is_active=True)
        tour_id = self.request.query_params.get('tour')
        if tour_id:
            queryset = queryset.filter(tour_id=tour_id)
        slot_date = self.request.query_params.get('date')
        if slot_date:
            try:
                d = date.fromisoformat(slot_date)
                queryset = queryset.filter(slot_date=d)
            except ValueError:
                pass
        return queryset.order_by('slot_date', 'start_time')

    def perform_create(self, serializer):
        guide_profile = getattr(self.request.user, 'guide_profile', None)
        serializer.save(guide=guide_profile)


# ----------------------------------------------------
# Concurrency Hold & Booking Engine
# ----------------------------------------------------

class BookingHoldCreateAPIView(APIView):
    """
    Acquires an atomic temporary hold lock (10 mins) on a room, tour, or slot.
    Uses select_for_update() inside a transaction to prevent double bookings.
    POST /api/bookings/hold/
    """
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            if 'room_type' in e.detail or 'tour_slot' in e.detail:
                err_msg = str(e.detail.get('room_type', e.detail.get('tour_slot', ['Slot unavailable']))[0])
                return Response({'error': err_msg}, status=status.HTTP_409_CONFLICT)
            raise e

        booking_type = serializer.validated_data.get('booking_type', 'TOUR')
        guests = serializer.validated_data.get('guests_count', 1)

        with transaction.atomic():
            if booking_type == 'HOTEL':
                room_type = serializer.validated_data['room_type']
                # Lock RoomType row
                locked_room = RoomType.objects.select_for_update().get(id=room_type.id)
                check_in = serializer.validated_data['check_in_date']
                check_out = serializer.validated_data['check_out_date']
                rooms_count = serializer.validated_data.get('rooms_count', 1)

                quote = locked_room.calculate_stay_quote(check_in, check_out, rooms_count)
                if not quote['is_available']:
                    return Response({'error': 'Room is no longer available for these dates.'}, status=status.HTTP_409_CONFLICT)

                total_price = Decimal(str(quote['total_price']))
                price_per_person = locked_room.base_price_per_night

            elif booking_type == 'ACTIVITY':
                slot = serializer.validated_data['tour_slot']
                # Lock TourSlot row
                locked_slot = TourSlot.objects.select_for_update().get(id=slot.id)
                if not locked_slot.is_available or locked_slot.remaining_capacity < guests:
                    return Response({'error': f'Slot only has {locked_slot.remaining_capacity} seats remaining.'}, status=status.HTTP_409_CONFLICT)

                locked_slot.booked_count += guests
                locked_slot.save(update_fields=['booked_count'])

                tour = locked_slot.tour
                price_per_person = tour.price_per_person
                total_price = price_per_person * guests

            else:
                tour = serializer.validated_data['tour']
                locked_tour = TourPackage.objects.select_for_update().get(id=tour.id)
                if guests > locked_tour.group_size_max:
                    return Response({'error': f'Exceeds max group size of {locked_tour.group_size_max}.'}, status=status.HTTP_400_BAD_REQUEST)

                price_per_person = locked_tour.price_per_person
                addons = serializer.validated_data.get('selected_addons', [])
                addons_total = sum(Decimal(str(a['price'])) for a in addons if isinstance(a, dict) and 'price' in a)
                total_price = (price_per_person * guests) + (addons_total * guests)

            # Create booking on hold for 10 minutes
            hold_expiry = timezone.now() + timedelta(minutes=10)
            user = request.user if request.user and request.user.is_authenticated else None

            booking = Booking.objects.create(
                user=user,
                booking_type=booking_type,
                tour=serializer.validated_data.get('tour'),
                room_type=serializer.validated_data.get('room_type'),
                tour_slot=serializer.validated_data.get('tour_slot'),
                customer_name=serializer.validated_data['customer_name'],
                customer_email=serializer.validated_data['customer_email'],
                customer_phone=serializer.validated_data['customer_phone'],
                departure_date=serializer.validated_data.get('departure_date'),
                check_in_date=serializer.validated_data.get('check_in_date'),
                check_out_date=serializer.validated_data.get('check_out_date'),
                rooms_count=serializer.validated_data.get('rooms_count', 1),
                guests_count=guests,
                price_per_person=price_per_person,
                selected_addons=serializer.validated_data.get('selected_addons', []),
                total_price=total_price,
                special_requests=serializer.validated_data.get('special_requests', ''),
                status='PENDING_HOLD',
                hold_expires_at=hold_expiry,
            )

        return Response({
            'message': 'Slot temporarily reserved. Please complete payment within 10 minutes.',
            'booking_reference': booking.booking_reference,
            'status': booking.status,
            'total_price': float(booking.total_price),
            'currency': 'USD',
            'hold_expires_at': booking.hold_expires_at.isoformat(),
            'hold_seconds_remaining': 600,
        }, status=status.HTTP_201_CREATED)


class BookingCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.select_related(
            'tour', 'tour__destination', 'room_type', 'room_type__hotel', 'tour_slot', 'invoice'
        ).order_by('-created_at')
        user = self.request.user
        
        if user.is_authenticated and user.role == 'TRAVELLER':
            return queryset.filter(Q(user=user) | Q(customer_email__iexact=user.email))
        
        email = self.request.query_params.get('email', '').strip()
        ref = self.request.query_params.get('reference', '').strip()
        if ref:
            queryset = queryset.filter(booking_reference__iexact=ref)
        elif email:
            queryset = queryset.filter(customer_email__iexact=email)
        return queryset

    def perform_create(self, serializer):
        if self.request.user and self.request.user.is_authenticated:
            booking = serializer.save(user=self.request.user)
        else:
            booking = serializer.save()
        generate_booking_invoice(booking)


class BookingDetailByReferenceAPIView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    lookup_field = 'booking_reference'

    def get_queryset(self):
        return Booking.objects.select_related(
            'tour', 'tour__destination', 'room_type', 'room_type__hotel', 'tour_slot', 'invoice'
        ).all()


class BookingCancelAPIView(APIView):
    """
    Cancels a booking, evaluates tiered refund policy, and triggers refund if applicable.
    POST /api/bookings/<booking_reference>/cancel/
    """
    def post(self, request, booking_reference):
        try:
            booking = Booking.objects.select_for_update().get(booking_reference__iexact=booking_reference)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status in ('CANCELLED', 'REFUNDED'):
            return Response({'error': f'Booking is already {booking.status.lower()}.'}, status=status.HTTP_400_BAD_REQUEST)

        reason = request.data.get('reason', 'Customer requested cancellation')
        refund_amount = booking.calculate_cancellation_refund()

        booking.status = 'REFUNDED' if refund_amount > 0 else 'CANCELLED'
        booking.cancellation_reason = reason
        booking.refund_amount = refund_amount
        booking.save()

        # If booking had a tour slot, restore the capacity
        if booking.tour_slot:
            slot = booking.tour_slot
            slot.booked_count = max(0, slot.booked_count - booking.guests_count)
            slot.save(update_fields=['booked_count'])

        # Process gateway refund if a captured transaction exists
        captured_tx = booking.payments.filter(status='CAPTURED').first()
        refund_id = None
        if captured_tx and refund_amount > 0:
            gateway = get_payment_gateway(captured_tx.provider)
            success, refund_res = gateway.process_refund(captured_tx, refund_amount, reason)
            if success:
                refund_id = refund_res
                PaymentTransaction.objects.create(
                    booking=booking,
                    provider=captured_tx.provider,
                    transaction_id=f"tx_rf_{uuid.uuid4().hex[:12]}",
                    external_order_id=captured_tx.external_order_id,
                    external_payment_id=refund_id,
                    amount=-refund_amount,
                    currency=captured_tx.currency,
                    status='REFUNDED',
                    raw_response={'refund_id': refund_id}
                )

        return Response({
            'message': 'Booking cancelled successfully.',
            'booking_reference': booking.booking_reference,
            'status': booking.status,
            'refund_amount': float(refund_amount),
            'cancellation_reason': reason,
            'refund_id': refund_id,
        }, status=status.HTTP_200_OK)


# ----------------------------------------------------
# Payment Order & Webhook Views
# ----------------------------------------------------

class PaymentOrderCreateAPIView(APIView):
    """
    Creates Stripe PaymentIntent or Razorpay Order for a booking in PENDING_HOLD.
    POST /api/payments/create-order/
    Body: {"booking_reference": "TRV-12345", "provider": "STRIPE" | "RAZORPAY"}
    """
    def post(self, request):
        ref = request.data.get('booking_reference')
        provider = request.data.get('provider', 'STRIPE').upper()

        if not ref:
            return Response({'error': 'booking_reference is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(booking_reference__iexact=ref)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status not in ('PENDING_HOLD', 'PENDING'):
            return Response({'error': f'Booking status is {booking.status}. Payment is not required.'}, status=status.HTTP_400_BAD_REQUEST)

        if booking.is_hold_expired:
            booking.status = 'CANCELLED'
            booking.save(update_fields=['status'])
            return Response({'error': 'Booking hold has expired. Please reserve the dates again.'}, status=status.HTTP_400_BAD_REQUEST)

        gateway = get_payment_gateway(provider)
        order_info = gateway.create_order(booking)

        # Record pending transaction
        PaymentTransaction.objects.create(
            booking=booking,
            provider=order_info['provider'],
            transaction_id=f"tx_{uuid.uuid4().hex[:14]}",
            external_order_id=order_info['order_id'],
            amount=booking.total_price,
            currency=order_info['currency'],
            status='PENDING',
            raw_response=order_info
        )

        return Response(order_info, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookAPIView(APIView):
    """
    Idempotent Stripe Webhook handler.
    POST /api/payments/webhook/stripe/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload_bytes = request.body
        sig_header = request.headers.get('Stripe-Signature', '')

        gateway = get_payment_gateway('STRIPE')
        valid, event = gateway.verify_webhook(payload_bytes, sig_header)
        if not valid:
            return Response({'error': 'Invalid signature.'}, status=status.HTTP_400_BAD_REQUEST)

        event_id = event.get('id', f"evt_sim_{uuid.uuid4().hex[:12]}")
        event_type = event.get('type', 'payment_intent.succeeded')

        # Idempotency check
        if PaymentWebhookLog.objects.filter(event_id=event_id).exists():
            return Response({'message': 'Webhook already processed.'}, status=status.HTTP_200_OK)

        webhook_log = PaymentWebhookLog.objects.create(
            event_id=event_id,
            provider='STRIPE',
            event_type=event_type,
            payload=event
        )

        if event_type in ('payment_intent.succeeded', 'charge.succeeded'):
            data_obj = event.get('data', {}).get('object', {})
            ref = data_obj.get('metadata', {}).get('booking_reference')
            payment_id = data_obj.get('id')

            if ref:
                with transaction.atomic():
                    try:
                        booking = Booking.objects.select_for_update().get(booking_reference__iexact=ref)
                        booking.status = 'CONFIRMED'
                        booking.save(update_fields=['status'])

                        # Generate invoice
                        generate_booking_invoice(booking)

                        # Update transaction status
                        tx = booking.payments.filter(provider='STRIPE').order_by('-created_at').first()
                        if tx:
                            tx.status = 'CAPTURED'
                            tx.external_payment_id = payment_id or ''
                            tx.save(update_fields=['status', 'external_payment_id'])

                        webhook_log.is_processed = True
                        webhook_log.save(update_fields=['is_processed'])
                    except Booking.DoesNotExist:
                        pass

        return Response({'received': True}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookAPIView(APIView):
    """
    Idempotent Razorpay Webhook handler.
    POST /api/payments/webhook/razorpay/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload_bytes = request.body
        sig_header = request.headers.get('X-Razorpay-Signature', '')

        gateway = get_payment_gateway('RAZORPAY')
        valid, event = gateway.verify_webhook(payload_bytes, sig_header)
        if not valid:
            return Response({'error': 'Invalid signature.'}, status=status.HTTP_400_BAD_REQUEST)

        event_id = event.get('id', f"evt_sim_{uuid.uuid4().hex[:12]}")
        event_type = event.get('event', 'payment.captured')

        if PaymentWebhookLog.objects.filter(event_id=event_id).exists():
            return Response({'message': 'Webhook already processed.'}, status=status.HTTP_200_OK)

        webhook_log = PaymentWebhookLog.objects.create(
            event_id=event_id,
            provider='RAZORPAY',
            event_type=event_type,
            payload=event
        )

        if event_type in ('payment.captured', 'order.paid'):
            payment_entity = event.get('payload', {}).get('payment', {}).get('entity', {})
            ref = payment_entity.get('notes', {}).get('booking_reference')
            payment_id = payment_entity.get('id')

            if ref:
                with transaction.atomic():
                    try:
                        booking = Booking.objects.select_for_update().get(booking_reference__iexact=ref)
                        booking.status = 'CONFIRMED'
                        booking.save(update_fields=['status'])

                        generate_booking_invoice(booking)

                        tx = booking.payments.filter(provider='RAZORPAY').order_by('-created_at').first()
                        if tx:
                            tx.status = 'CAPTURED'
                            tx.external_payment_id = payment_id or ''
                            tx.save(update_fields=['status', 'external_payment_id'])

                        webhook_log.is_processed = True
                        webhook_log.save(update_fields=['is_processed'])
                    except Booking.DoesNotExist:
                        pass

        return Response({'received': True}, status=status.HTTP_200_OK)


class InvoiceDetailAPIView(APIView):
    """
    Retrieves tax invoice & digital boarding pass receipt for a booking.
    GET /api/bookings/<booking_reference>/invoice/
    """
    def get(self, request, booking_reference):
        try:
            booking = Booking.objects.select_related('tour', 'room_type__hotel', 'invoice').get(
                booking_reference__iexact=booking_reference
            )
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        invoice = generate_booking_invoice(booking)
        serializer = InvoiceSerializer(invoice)
        data = serializer.data
        data['booking_reference'] = booking.booking_reference
        data['customer_name'] = booking.customer_name
        data['status'] = booking.status
        data['item_title'] = booking.tour.title if booking.tour else (booking.room_type.hotel.name if booking.room_type else "Voyage Reservation")
        return Response(data, status=status.HTTP_200_OK)


# ----------------------------------------------------
# General Views & Reviews
# ----------------------------------------------------

class TourReviewCreateAPIView(APIView):
    def post(self, request, tour_id):
        try:
            tour = TourPackage.objects.get(id=tour_id)
        except TourPackage.DoesNotExist:
            return Response({'error': 'Tour package not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['tour'] = tour.id
        if request.user and request.user.is_authenticated:
            data['user'] = request.user.id
            if not data.get('author_name'):
                data['author_name'] = request.user.full_name or request.user.email.split('@')[0]
            if not data.get('author_avatar'):
                data['author_avatar'] = request.user.avatar_url

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            reviews = tour.reviews.all()
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 5.0
            tour.rating = round(avg_rating, 1)
            tour.review_count = reviews.count()
            tour.save(update_fields=['rating', 'review_count'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatsOverviewAPIView(APIView):
    def get(self, request):
        destination_count = Destination.objects.count()
        tour_count = TourPackage.objects.count()
        hotel_count = Hotel.objects.count()
        booking_count = Booking.objects.count()
        user_count = User.objects.count()
        avg_rating = TourPackage.objects.aggregate(Avg('rating'))['rating__avg'] or 4.9
        categories = list(TourPackage.objects.values_list('category', flat=True).distinct())

        return Response({
            'total_destinations': destination_count,
            'total_tours': tour_count,
            'total_hotels': hotel_count,
            'total_bookings': booking_count + 1420,
            'total_users': user_count + 3200,
            'average_rating': round(avg_rating, 2),
            'categories': categories,
            'satisfaction_rate': '99.2%'
        })


class AdminDashboardAnalyticsAPIView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        total_revenue = Booking.objects.filter(status='CONFIRMED').aggregate(Sum('total_price'))['total_price__sum'] or Decimal(0)
        confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
        pending_bookings = Booking.objects.filter(status__in=['PENDING_HOLD', 'PAYMENT_PROCESSING']).count()
        cancelled_bookings = Booking.objects.filter(status__in=['CANCELLED', 'REFUNDED']).count()

        roles_breakdown = dict(User.objects.values('role').annotate(count=Count('id')).values_list('role', 'count'))

        return Response({
            'total_revenue': float(total_revenue),
            'confirmed_bookings': confirmed_bookings,
            'pending_bookings': pending_bookings,
            'cancelled_bookings': cancelled_bookings,
            'users_by_role': roles_breakdown,
        })
