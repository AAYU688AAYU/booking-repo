from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Destination, TourPackage, Booking, Review


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_verified', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'avatar_url', 'role', 'is_verified', 'google_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'full_name'),
        }),
    )


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
    list_display = ('booking_reference', 'customer_name', 'user', 'tour', 'departure_date', 'guests_count', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'departure_date')
    search_fields = ('booking_reference', 'customer_name', 'customer_email', 'tour__title')
    readonly_fields = ('booking_reference', 'created_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'tour', 'user', 'rating', 'travel_type', 'created_at')
    list_filter = ('rating', 'travel_type')
    search_fields = ('author_name', 'tour__title', 'title', 'comment')
