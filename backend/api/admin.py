from django.contrib import admin
from .models import Destination, TourPackage, Booking, Review


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'region', 'climate', 'best_season', 'is_featured')
    list_filter = ('region', 'is_featured')
    search_fields = ('name', 'country')


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'category', 'duration_days', 'price_per_person', 'rating', 'is_featured', 'is_trending')
    list_filter = ('category', 'difficulty', 'is_featured', 'is_trending', 'destination__region')
    search_fields = ('title', 'destination__name', 'destination__country')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'customer_name', 'tour', 'departure_date', 'guests_count', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'departure_date')
    search_fields = ('booking_reference', 'customer_name', 'customer_email', 'tour__title')
    readonly_fields = ('booking_reference', 'created_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'tour', 'rating', 'travel_type', 'created_at')
    list_filter = ('rating', 'travel_type')
    search_fields = ('author_name', 'tour__title', 'title', 'comment')
