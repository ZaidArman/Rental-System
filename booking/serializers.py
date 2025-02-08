from rest_framework import serializers
from .models import Car, Booking, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "user",  # Optional: Exclude this if you don't want it in the response
            "customer_first_name",
            "customer_last_name",
            "address",
            "cnic",
            "contact_number",
            "email",
            "car",
            "from_date",
            "to_date",
            "status",
        ]
        read_only_fields = ["status", "user"]  # Prevent user and status from being updated manually


    # def validate(self, data):
    #     car = data.get('car')
    #     from_date = data.get('from_date')
    #     to_date = data.get('to_date')

    #     # Check for overlapping bookings
    #     overlapping_bookings = Booking.objects.filter(
    #         car=car,
    #         status='CONFIRMED',
    #         from_date__lt=to_date,
    #         to_date__gt=from_date,
    #     ).exists()

    #     if overlapping_bookings:
    #         raise serializers.ValidationError("This car is not available for the selected dates.")
    #     return data
