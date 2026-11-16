from decimal import Decimal
from rest_framework import serializers
from .models import Destination, TourPackage, Booking, Review


class ReviewSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.DateTimeField(source='created_at', format='%b %d, %Y', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'tour', 'author_name', 'author_avatar',
            'author_country', 'travel_type', 'rating',
            'title', 'comment', 'created_at', 'created_at_formatted'
        ]
        read_only_fields = ['id', 'created_at']


class DestinationSerializer(serializers.ModelSerializer):
    tour_count = serializers.IntegerField(source='tours.count', read_only=True)

    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'country', 'region', 'description',
            'image_url', 'climate', 'best_season', 'is_featured', 'tour_count'
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


class BookingSerializer(serializers.ModelSerializer):
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    tour_destination = serializers.CharField(source='tour.destination.name', read_only=True)
    tour_image = serializers.URLField(source='tour.image_url', read_only=True)
    tour_duration = serializers.IntegerField(source='tour.duration_days', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_reference', 'tour', 'tour_title', 'tour_destination', 'tour_image',
            'tour_duration', 'customer_name', 'customer_email', 'customer_phone',
            'departure_date', 'guests_count', 'price_per_person', 'selected_addons',
            'total_price', 'special_requests', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'booking_reference', 'price_per_person', 'total_price', 'status', 'created_at']

    def validate(self, attrs):
        tour = attrs.get('tour')
        guests = attrs.get('guests_count', 1)
        if guests < 1:
            raise serializers.ValidationError({"guests_count": "At least 1 guest is required."})
        if tour and guests > tour.group_size_max:
            raise serializers.ValidationError({"guests_count": f"Maximum allowed guests for this package is {tour.group_size_max}."})
        return attrs

    def create(self, validated_data):
        tour = validated_data['tour']
        guests = validated_data.get('guests_count', 1)
        price_per_person = tour.price_per_person
        
        # Calculate add-on cost
        addons = validated_data.get('selected_addons', [])
        addons_total = Decimal(0)
        for addon in addons:
            if isinstance(addon, dict) and 'price' in addon:
                addons_total += Decimal(str(addon['price']))

        total_price = (price_per_person * guests) + (addons_total * guests)
        
        validated_data['price_per_person'] = price_per_person
        validated_data['total_price'] = total_price
        validated_data['status'] = 'CONFIRMED'
        return super().create(validated_data)
