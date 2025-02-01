from django.db import models
from django.conf import settings

class Car(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Status(models.TextChoices):
    PENDING = 'P', 'Pending'
    APPROVED = 'A', 'Approved'
    CANCELLED = 'C', 'Cancelled'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    customer_first_name = models.CharField(max_length=100)
    customer_last_name = models.CharField(max_length=100)
    address = models.TextField()
    cnic = models.CharField(max_length=15)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="bookings")
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(
        max_length=1, 
        choices=Status.choices, 
        default=Status.PENDING
    )

    def __str__(self):
        return f"Booking for {self.car.name} by {self.user.username}"
