from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    SUPER_ADMIN = 'Super Admin'
    ADMIN = 'Rental'
    ACCOUNTANT = 'Customer'
    ROLES = (
        (SUPER_ADMIN, _('Super Admin')),
        (ADMIN, _('Rental')),
        (ACCOUNTANT, _('Customer')),
    )
    username = None
    email = models.EmailField(null=True, blank=True, unique=True)
    cnic = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    address = models.TextField()
    created_at = models.DateField(null=True, blank=True, auto_now=True, editable=True)
    roles = models.CharField(max_length=50, choices=ROLES, default=SUPER_ADMIN)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'  
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email  