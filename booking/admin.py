from django.contrib import admin
from .models import Car, Booking

# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_available']
    list_filter = ['is_available']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['car', 'customer_first_name', 'from_date', 'to_date']
    list_filter = ['from_date', 'to_date', 'car']
