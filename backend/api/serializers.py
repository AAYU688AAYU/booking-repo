from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Destination, TourPackage, Hotel, RoomType,
    SeasonalPricing, RoomInventory, GuideProfile, TourSlot,
    Booking, Review
)

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = user.full_name
        token['role'] = user.role
        token['is_verified'] = user.is_verified
        token['avatar_url'] = user.avatar_url
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
            'role': self.user.role,
            'phone_number': self.user.phone_number,
            'is_verified': self.user.is_verified,
            'avatar_url': self.user.avatar_url,
        }
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password_confirm', 'full_name', 'phone_number', 'role']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'role', 'is_verified', 'avatar_url', 'date_joined']
        read_only_fields = ['id', 'email', 'role', 'is_verified', 'date_joined']


class GoogleAuthSerializer(serializers.Serializer):
    credential = serializers.CharField(required=True)
    role = serializers.CharField(required=False, default='TRAVELLER')


class ReviewSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.DateTimeField(source='created_at', format='%b %d, %Y', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'tour', 'hotel', 'user', 'author_name', 'author_avatar',
            'author_country', 'travel_type', 'rating',
            'title', 'comment', 'created_at', 'created_at_formatted'
        ]
        read_only_fields = ['id', 'created_at']


class DestinationSerializer(serializers.ModelSerializer):
    tour_count = serializers.IntegerField(source='tours.count', read_only=True)
    hotel_count = serializers.IntegerField(source='hotels.count', read_only=True)

    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'country', 'region', 'description',
            'image_url', 'climate', 'best_season', 'is_featured', 'tour_count', 'hotel_count'
        ]


class TourPackageListSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_country = serializers.CharField(source='destination.country', read_only=True)
    destination_region = serializers.CharField(source='destination.region', read_only=True)

    class Meta:
        model = TourPackage
        fields = [
            'id', 'destination', 'destination_name', 'destination_country', 'destination_region',
            'title', 'slug', 'category', 'duration_days', 'travel_time',
            'price_per_person', 'original_price', 'group_size_max',
            'difficulty', 'rating', 'review_count', 'short_description',
            'image_url', 'highlights', 'is_featured', 'is_trending'
        ]


class TourPackageDetailSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = TourPackage
        fields = [
            'id', 'destination', 'title', 'slug', 'category', 'duration_days', 'travel_time',
            'price_per_person', 'original_price', 'group_size_max',
            'difficulty', 'rating', 'review_count', 'short_description',
            'detailed_overview', 'image_url', 'gallery_urls', 'highlights',
            'included', 'excluded', 'itinerary', 'upcoming_dates',
            'is_featured', 'is_trending', 'reviews'
        ]


# ----------------------------------------------------
# Hotels & Accommodation Serializers
# ----------------------------------------------------

class SeasonalPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalPricing
        fields = ['id', 'name', 'start_date', 'end_date', 'price_multiplier', 'fixed_price']


class RoomTypeSerializer(serializers.ModelSerializer):
    seasonal_prices = SeasonalPricingSerializer(many=True, read_only=True)

    class Meta:
        model = RoomType
        fields = [
            'id', 'hotel', 'name', 'slug', 'description', 'max_occupancy',
            'base_price_per_night', 'total_rooms', 'bed_type', 'room_size_sqm',
            'image_url', 'amenities', 'seasonal_prices'
        ]


class HotelListSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_country = serializers.CharField(source='destination.country', read_only=True)
    destination_region = serializers.CharField(source='destination.region', read_only=True)
    min_price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    rooms_count = serializers.IntegerField(source='room_types.count', read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id', 'destination', 'destination_name', 'destination_country', 'destination_region',
            'name', 'slug', 'address', 'star_rating', 'description',
            'image_url', 'amenities', 'check_in_time', 'check_out_time',
            'min_price_per_night', 'rooms_count', 'is_featured'
        ]


class HotelDetailSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    room_types = RoomTypeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id', 'destination', 'name', 'slug', 'address', 'star_rating',
            'description', 'image_url', 'gallery_urls', 'amenities',
            'check_in_time', 'check_out_time', 'is_featured',
            'room_types', 'reviews'
        ]


class GuideProfileSerializer(serializers.ModelSerializer):
    guide_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    avatar_url = serializers.URLField(source='user.avatar_url', read_only=True)

    class Meta:
        model = GuideProfile
        fields = [
            'id', 'user', 'guide_name', 'email', 'avatar_url', 'bio',
            'license_number', 'spoken_languages', 'experience_years',
            'rating', 'review_count', 'is_verified'
        ]


class TourSlotSerializer(serializers.ModelSerializer):
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    guide_name = serializers.CharField(source='guide.user.full_name', read_only=True)
    remaining_capacity = serializers.IntegerField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = TourSlot
        fields = [
            'id', 'tour', 'tour_title', 'guide', 'guide_name', 'slot_date',
            'start_time', 'end_time', 'max_capacity', 'booked_count',
            'remaining_capacity', 'is_available', 'is_active'
        ]


# ----------------------------------------------------
# Unified Booking Serializer
# ----------------------------------------------------

class BookingSerializer(serializers.ModelSerializer):
    item_title = serializers.SerializerMethodField()
    item_image = serializers.SerializerMethodField()
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    hotel_name = serializers.CharField(source='room_type.hotel.name', read_only=True)
    room_name = serializers.CharField(source='room_type.name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_reference', 'booking_type', 'user',
            'tour', 'room_type', 'tour_slot',
            'item_title', 'item_image', 'tour_title', 'hotel_name', 'room_name',
            'customer_name', 'customer_email', 'customer_phone',
            'departure_date', 'check_in_date', 'check_out_date', 'rooms_count',
            'guests_count', 'price_per_person', 'selected_addons',
            'total_price', 'special_requests', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'booking_reference', 'total_price', 'status', 'created_at']

    def get_item_title(self, obj):
        if obj.tour:
            return obj.tour.title
        if obj.room_type:
            return f"{obj.room_type.hotel.name} - {obj.room_type.name}"
        return "Booking Reservation"

    def get_item_image(self, obj):
        if obj.tour:
            return obj.tour.image_url
        if obj.room_type:
            return obj.room_type.image_url or obj.room_type.hotel.image_url
        return ""

    def validate(self, attrs):
        booking_type = attrs.get('booking_type', 'TOUR')
        guests = attrs.get('guests_count', 1)
        if guests < 1:
            raise serializers.ValidationError({"guests_count": "At least 1 guest is required."})

        if booking_type == 'HOTEL':
            room_type = attrs.get('room_type')
            check_in = attrs.get('check_in_date')
            check_out = attrs.get('check_out_date')
            rooms_count = attrs.get('rooms_count', 1)

            if not room_type:
                raise serializers.ValidationError({"room_type": "Room type is required for hotel bookings."})
            if not check_in or not check_out:
                raise serializers.ValidationError({"dates": "Both check-in and check-out dates are required."})
            if check_out <= check_in:
                raise serializers.ValidationError({"check_out_date": "Check-out date must be strictly after check-in date."})

            quote = room_type.calculate_stay_quote(check_in, check_out, rooms_count)
            if not quote['is_available']:
                raise serializers.ValidationError({"room_type": "Selected room is not available for all nights in this date range."})
            
            # Cache computed total on attrs for create()
            attrs['_computed_total'] = Decimal(str(quote['total_price']))

        elif booking_type == 'ACTIVITY':
            slot = attrs.get('tour_slot')
            if not slot:
                raise serializers.ValidationError({"tour_slot": "Tour slot is required for activity bookings."})
            if not slot.is_available or slot.remaining_capacity < guests:
                raise serializers.ValidationError({"tour_slot": f"Selected slot has only {slot.remaining_capacity} seats remaining."})
            tour = slot.tour
            attrs['tour'] = tour
            attrs['departure_date'] = slot.slot_date

        elif booking_type == 'TOUR':
            tour = attrs.get('tour')
            if not tour:
                raise serializers.ValidationError({"tour": "Tour package is required for tour bookings."})
            if guests > tour.group_size_max:
                raise serializers.ValidationError({"guests_count": f"Maximum allowed guests for this package is {tour.group_size_max}."})

        return attrs

    def create(self, validated_data):
        computed_total = validated_data.pop('_computed_total', None)
        booking_type = validated_data.get('booking_type', 'TOUR')
        guests = validated_data.get('guests_count', 1)

        if booking_type == 'HOTEL':
            total_price = computed_total
            validated_data['price_per_person'] = validated_data['room_type'].base_price_per_night
            validated_data['total_price'] = total_price
        else:
            tour = validated_data.get('tour')
            price_per_person = tour.price_per_person if tour else Decimal('0.00')
            addons = validated_data.get('selected_addons', [])
            addons_total = Decimal(0)
            for addon in addons:
                if isinstance(addon, dict) and 'price' in addon:
                    addons_total += Decimal(str(addon['price']))

            total_price = (price_per_person * guests) + (addons_total * guests)
            validated_data['price_per_person'] = price_per_person
            validated_data['total_price'] = total_price

        validated_data['status'] = 'CONFIRMED'
        booking = super().create(validated_data)

        # Update slot or inventory booked counters
        if booking.tour_slot:
            slot = booking.tour_slot
            slot.booked_count += guests
            slot.save(update_fields=['booked_count'])

        return booking
