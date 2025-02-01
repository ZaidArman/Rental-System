from django.urls import path
from .views import (
    CarListView,
    BookingCreateView,
    BookingUpdateView,
    BookingConfirmView,
)

urlpatterns = [
    path('cars/', CarListView.as_view(), name='car-list'),
    path('book/', BookingCreateView.as_view(), name='booking-create'),
    path('book/<int:pk>/', BookingUpdateView.as_view(), name='booking-update'),
    path('book/<int:pk>/confirm/', BookingConfirmView.as_view(), name='booking-confirm'),
]
