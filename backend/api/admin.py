from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Destination, TourPackage, Hotel, RoomType,
    SeasonalPricing, RoomInventory, GuideProfile, TourSlot,
    Booking, Review
)


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


class RoomTypeInline(admin.TabularInline):
    model = RoomType
    extra = 1
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'owner', 'star_rating', 'is_featured', 'created_at')
    list_filter = ('star_rating', 'is_featured', 'destination__region')
    search_fields = ('name', 'destination__name', 'destination__country', 'address')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RoomTypeInline]


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'base_price_per_night', 'max_occupancy', 'total_rooms', 'bed_type')
    list_filter = ('hotel', 'max_occupancy')
    search_fields = ('name', 'hotel__name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SeasonalPricing)
class SeasonalPricingAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'start_date', 'end_date', 'price_multiplier', 'fixed_price')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'room_type__name', 'room_type__hotel__name')


@admin.register(RoomInventory)
class RoomInventoryAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'date', 'booked_rooms', 'is_blocked')
    list_filter = ('date', 'is_blocked')
    search_fields = ('room_type__name', 'room_type__hotel__name')


@admin.register(GuideProfile)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'experience_years', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'rating')
    search_fields = ('user__full_name', 'user__email', 'bio')


@admin.register(TourSlot)
class TourSlotAdmin(admin.ModelAdmin):
    list_display = ('tour', 'guide', 'slot_date', 'start_time', 'booked_count', 'max_capacity', 'is_active')
    list_filter = ('slot_date', 'is_active')
    search_fields = ('tour__title', 'guide__user__full_name')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'customer_name', 'booking_type', 'user', 'tour', 'room_type', 'status', 'total_price', 'created_at')
    list_filter = ('booking_type', 'status', 'created_at')
    search_fields = ('booking_reference', 'customer_name', 'customer_email', 'tour__title', 'room_type__name')
    readonly_fields = ('booking_reference', 'created_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'tour', 'hotel', 'user', 'rating', 'travel_type', 'created_at')
    list_filter = ('rating', 'travel_type')
    search_fields = ('author_name', 'tour__title', 'hotel__name', 'title', 'comment')
