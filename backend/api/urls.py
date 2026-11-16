from django.urls import path
from .views import (
    DestinationListAPIView,
    TourPackageListAPIView,
    TourPackageDetailAPIView,
    BookingCreateListAPIView,
    BookingDetailByReferenceAPIView,
    TourReviewCreateAPIView,
    StatsOverviewAPIView
)

urlpatterns = [
    path('destinations/', DestinationListAPIView.as_view(), name='destination-list'),
    path('trips/', TourPackageListAPIView.as_view(), name='trip-list'),
    path('trips/<int:id>/', TourPackageDetailAPIView.as_view(), name='trip-detail'),
    path('trips/<int:tour_id>/reviews/', TourReviewCreateAPIView.as_view(), name='trip-add-review'),
    path('bookings/', BookingCreateListAPIView.as_view(), name='booking-create-list'),
    path('bookings/<str:booking_reference>/', BookingDetailByReferenceAPIView.as_view(), name='booking-detail-ref'),
    path('stats/', StatsOverviewAPIView.as_view(), name='platform-stats'),
]
