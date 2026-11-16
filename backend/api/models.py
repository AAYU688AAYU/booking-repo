import random
import string
from datetime import date, timedelta
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


def generate_booking_reference():
    digits = ''.join(random.choices(string.digits, k=5))
    return f"TRV-{digits}"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('TRAVELLER', 'Traveller'),
        ('VENDOR', 'Hotel & Accommodation Vendor'),
        ('GUIDE', 'Tour Guide'),
        ('ADMIN', 'Platform Administrator'),
    ]

    username = None  # Use email as unique identifier
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TRAVELLER')
    is_verified = models.BooleanField(default=False)
    avatar_url = models.URLField(max_length=500, blank=True)
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"


class Destination(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)  # Europe, Asia, Americas, Africa, Oceania
    description = models.TextField()
    image_url = models.URLField(max_length=500)
    climate = models.CharField(max_length=100, default='Pleasant')
    best_season = models.CharField(max_length=100, default='Spring - Autumn')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.country}"


class TourPackage(models.Model):
    CATEGORY_CHOICES = [
        ('Student', 'Student & Backpacker Special'),
        ('Budget', 'Budget & Pocket-Friendly'),
        ('Adventure', 'Adventure & Trekking'),
        ('Cultural', 'Cultural & Heritage'),
        ('Relaxation', 'Coastal & Relaxation'),
        ('Wildlife', 'Safari & Wildlife'),
        ('Luxury', 'Luxury & Scenic'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy - Leisurely pace'),
        ('Moderate', 'Moderate - Some physical activity'),
        ('Challenging', 'Challenging - Active hiking/trekking'),
    ]

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tours')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Cultural')
    duration_days = models.PositiveIntegerField(default=5)
    travel_time = models.CharField(max_length=255, default='', blank=True, help_text='Transit time from major hub, e.g., 7 hrs from Delhi by Volvo')
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    group_size_max = models.PositiveIntegerField(default=12)
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, default='Easy')
    rating = models.FloatField(default=4.9)
    review_count = models.PositiveIntegerField(default=0)
    
    short_description = models.TextField()
    detailed_overview = models.TextField()
    image_url = models.URLField(max_length=500)
    gallery_urls = models.JSONField(default=list, blank=True)
    highlights = models.JSONField(default=list, blank=True)
    included = models.JSONField(default=list, blank=True)
    excluded = models.JSONField(default=list, blank=True)
    itinerary = models.JSONField(default=list, blank=True)
    upcoming_dates = models.JSONField(default=list, blank=True)

    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ----------------------------------------------------
# Hotels & Accommodation Module
# ----------------------------------------------------

class Hotel(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='hotels')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='hotels')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    address = models.CharField(max_length=300)
    star_rating = models.PositiveSmallIntegerField(default=4)
    description = models.TextField()
    image_url = models.URLField(max_length=500)
    gallery_urls = models.JSONField(default=list, blank=True)
    amenities = models.JSONField(default=list, blank=True)  # e.g. ["Free WiFi", "Infinity Pool", "Spa", "Valet Parking"]
    check_in_time = models.CharField(max_length=50, default='14:00')
    check_out_time = models.CharField(max_length=50, default='11:00')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.destination.name})"

    @property
    def min_price_per_night(self):
        lowest_room = self.room_types.order_by('base_price_per_night').first()
        return lowest_room.base_price_per_night if lowest_room else Decimal('0.00')


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=150)  # e.g., "Deluxe Ocean Suite", "Presidential King"
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    max_occupancy = models.PositiveIntegerField(default=2)
    base_price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.PositiveIntegerField(default=10)
    bed_type = models.CharField(max_length=100, default='1 King Bed')
    room_size_sqm = models.PositiveIntegerField(default=35)
    image_url = models.URLField(max_length=500, blank=True)
    amenities = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ('hotel', 'slug')

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"

    def calculate_stay_quote(self, start_date: date, end_date: date, requested_rooms: int = 1):
        """
        Calculates day-by-day availability and dynamic price across date range.
        Returns dict with: is_available, available_rooms, total_price, nightly_breakdown
        """
        if start_date >= end_date:
            return {'is_available': False, 'error': 'Checkout date must be after check-in date.'}

        days_count = (end_date - start_date).days
        current = start_date
        nightly_breakdown = []
        total_price = Decimal('0.00')
        min_available = self.total_rooms

        # Fetch seasonal pricing rules that overlap with range
        seasonal_rules = list(self.seasonal_prices.filter(
            start_date__lte=end_date,
            end_date__gte=start_date
        ))

        # Fetch daily inventory entries
        inventory_map = {
            inv.date: inv for inv in self.daily_inventory.filter(
                date__gte=start_date,
                date__lt=end_date
            )
        }

        while current < end_date:
            inv = inventory_map.get(current)
            booked = inv.booked_rooms if inv else 0
            is_blocked = inv.is_blocked if inv else False

            available = max(0, self.total_rooms - booked)
            if is_blocked or available < requested_rooms:
                min_available = 0
            else:
                min_available = min(min_available, available)

            # Determine daily price (seasonal multiplier or fixed price)
            day_price = self.base_price_per_night
            active_season = None
            for season in seasonal_rules:
                if season.start_date <= current <= season.end_date:
                    if season.fixed_price:
                        day_price = season.fixed_price
                    else:
                        day_price = day_price * season.price_multiplier
                    active_season = season.name
                    break

            daily_subtotal = day_price * requested_rooms
            total_price += daily_subtotal

            nightly_breakdown.append({
                'date': current.isoformat(),
                'base_rate': float(self.base_price_per_night),
                'effective_rate': float(day_price),
                'available_rooms': available,
                'seasonal_rule': active_season,
            })
            current += timedelta(days=1)

        is_available = min_available >= requested_rooms
        return {
            'is_available': is_available,
            'available_rooms': min_available,
            'nights_count': days_count,
            'total_price': float(total_price),
            'currency': 'USD',
            'nightly_breakdown': nightly_breakdown,
        }


class SeasonalPricing(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='seasonal_prices')
    name = models.CharField(max_length=100)  # e.g., "Peak Summer Season", "Holiday Surge"
    start_date = models.DateField()
    end_date = models.DateField()
    price_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('1.00'))
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.room_type.name} - {self.name} ({self.start_date} to {self.end_date})"


class RoomInventory(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='daily_inventory')
    date = models.DateField()
    booked_rooms = models.PositiveIntegerField(default=0)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room_type', 'date')
        indexes = [
            models.Index(fields=['room_type', 'date']),
        ]

    def __str__(self):
        return f"{self.room_type.name} on {self.date}: {self.booked_rooms} booked"


# ----------------------------------------------------
# Tour Guides & Activities Module
# ----------------------------------------------------

class GuideProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guide_profile')
    bio = models.TextField()
    license_number = models.CharField(max_length=100, blank=True)
    spoken_languages = models.JSONField(default=list, blank=True)  # e.g. ["English", "Spanish", "French"]
    experience_years = models.PositiveIntegerField(default=3)
    rating = models.FloatField(default=5.0)
    review_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=True)
    destinations = models.ManyToManyField(Destination, related_name='guides', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Guide: {self.user.full_name or self.user.email} ({self.rating}★)"


class TourSlot(models.Model):
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='slots')
    guide = models.ForeignKey(GuideProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='slots')
    slot_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    max_capacity = models.PositiveIntegerField(default=12)
    booked_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['slot_date', 'start_time']

    def __str__(self):
        return f"{self.tour.title} on {self.slot_date} at {self.start_time}"

    @property
    def remaining_capacity(self):
        return max(0, self.max_capacity - self.booked_count)

    @property
    def is_available(self):
        return self.is_active and self.remaining_capacity > 0


# ----------------------------------------------------
# Unified Booking Model
# ----------------------------------------------------

class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('PENDING', 'Pending Payment'),
        ('CANCELLED', 'Cancelled'),
    ]

    BOOKING_TYPE_CHOICES = [
        ('TOUR', 'Tour Expedition'),
        ('HOTEL', 'Hotel & Accommodation'),
        ('ACTIVITY', 'Guided Tour Slot'),
    ]

    booking_reference = models.CharField(max_length=20, unique=True, editable=False)
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, default='TOUR')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    tour_slot = models.ForeignKey(TourSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')

    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=50)

    # Date semantics: departure_date for tours, check_in_date / check_out_date for hotels
    departure_date = models.DateField(null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    rooms_count = models.PositiveIntegerField(default=1)

    guests_count = models.PositiveIntegerField(default=1)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    selected_addons = models.JSONField(default=list, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_requests = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            while True:
                ref = generate_booking_reference()
                if not Booking.objects.filter(booking_reference=ref).exists():
                    self.booking_reference = ref
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        title = self.tour.title if self.tour else (self.room_type.hotel.name if self.room_type else "Booking")
        return f"{self.booking_reference} - {self.customer_name} ({title})"


class Review(models.Model):
    TRAVEL_TYPE_CHOICES = [
        ('Solo', 'Solo Traveller'),
        ('Couple', 'Couple'),
        ('Family', 'Family'),
        ('Friends', 'Friends'),
    ]

    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    author_name = models.CharField(max_length=120)
    author_avatar = models.URLField(max_length=500, blank=True)
    author_country = models.CharField(max_length=100, blank=True, default='Global Citizen')
    travel_type = models.CharField(max_length=20, choices=TRAVEL_TYPE_CHOICES, default='Couple')
    rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.tour.title if self.tour else (self.hotel.name if self.hotel else "Review")
        return f"{self.rating}★ by {self.author_name} for {target}"
