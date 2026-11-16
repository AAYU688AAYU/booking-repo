import random
import string
from django.db import models


def generate_booking_reference():
    digits = ''.join(random.choices(string.digits, k=5))
    return f"TRV-{digits}"


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


class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('PENDING', 'Pending Payment'),
        ('CANCELLED', 'Cancelled'),
    ]

    booking_reference = models.CharField(max_length=20, unique=True, editable=False)
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=50)
    departure_date = models.DateField()
    guests_count = models.PositiveIntegerField(default=1)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    selected_addons = models.JSONField(default=list, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_requests = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Ensure unique reference code
            while True:
                ref = generate_booking_reference()
                if not Booking.objects.filter(booking_reference=ref).exists():
                    self.booking_reference = ref
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference} - {self.customer_name} ({self.tour.title})"


class Review(models.Model):
    TRAVEL_TYPE_CHOICES = [
        ('Solo', 'Solo Traveller'),
        ('Couple', 'Couple'),
        ('Family', 'Family'),
        ('Friends', 'Friends'),
    ]

    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='reviews')
    author_name = models.CharField(max_length=120)
    author_avatar = models.URLField(max_length=500, blank=True)
    author_country = models.CharField(max_length=100, blank=True, default='Global Citizen')
    travel_type = models.CharField(max_length=20, choices=TRAVEL_TYPE_CHOICES, default='Couple')
    rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}★ by {self.author_name} for {self.tour.title}"
