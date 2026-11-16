from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterAPIView,
    CustomTokenObtainPairView,
    UserProfileAPIView,
    GoogleAuthAPIView,
    DestinationListAPIView,
    TourPackageListAPIView,
    TourPackageDetailAPIView,
    HotelListCreateAPIView,
    HotelDetailAPIView,
    RoomAvailabilityQuoteAPIView,
    GuideListAPIView,
    GuideDetailAPIView,
    TourSlotListCreateAPIView,
    BookingCreateListAPIView,
    BookingDetailByReferenceAPIView,
    TourReviewCreateAPIView,
    StatsOverviewAPIView,
    AdminDashboardAnalyticsAPIView,
)

urlpatterns = [
    # Authentication & User Profiles
    path('auth/register/', RegisterAPIView.as_view(), name='auth-register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='auth-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('auth/profile/', UserProfileAPIView.as_view(), name='auth-profile'),
    path('auth/google/', GoogleAuthAPIView.as_view(), name='auth-google'),

    # Destinations & Tours
    path('destinations/', DestinationListAPIView.as_view(), name='destination-list'),
    path('trips/', TourPackageListAPIView.as_view(), name='trip-list'),
    path('trips/<int:id>/', TourPackageDetailAPIView.as_view(), name='trip-detail'),
    path('trips/<int:tour_id>/reviews/', TourReviewCreateAPIView.as_view(), name='trip-add-review'),

    # Hotels & Accommodations
    path('hotels/', HotelListCreateAPIView.as_view(), name='hotel-list-create'),
    path('hotels/<int:id>/', HotelDetailAPIView.as_view(), name='hotel-detail'),
    path('hotels/<int:hotel_id>/rooms/<int:room_id>/availability/', RoomAvailabilityQuoteAPIView.as_view(), name='room-availability-quote'),

    # Tour Guides & Activities
    path('guides/', GuideListAPIView.as_view(), name='guide-list'),
    path('guides/<int:id>/', GuideDetailAPIView.as_view(), name='guide-detail'),
    path('slots/', TourSlotListCreateAPIView.as_view(), name='tour-slot-list-create'),

    # Bookings Engine
    path('bookings/', BookingCreateListAPIView.as_view(), name='booking-create-list'),
    path('bookings/<str:booking_reference>/', BookingDetailByReferenceAPIView.as_view(), name='booking-detail-ref'),

    # Platform Metrics & RBAC Analytics
    path('stats/', StatsOverviewAPIView.as_view(), name='platform-stats'),
    path('admin/analytics/', AdminDashboardAnalyticsAPIView.as_view(), name='admin-analytics'),
]
