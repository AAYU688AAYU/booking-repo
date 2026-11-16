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

    # Bookings Engine
    path('bookings/', BookingCreateListAPIView.as_view(), name='booking-create-list'),
    path('bookings/<str:booking_reference>/', BookingDetailByReferenceAPIView.as_view(), name='booking-detail-ref'),

    # Platform Metrics & RBAC Analytics
    path('stats/', StatsOverviewAPIView.as_view(), name='platform-stats'),
    path('admin/analytics/', AdminDashboardAnalyticsAPIView.as_view(), name='admin-analytics'),
]
