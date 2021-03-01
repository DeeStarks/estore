from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from store.models import CATEGORIES

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mobile = PhoneNumberField(null=True, blank=True, unique=True)
    permanent_address = models.CharField(max_length=400, null=True)
    shipping_address = models.CharField(max_length=400, null=True)

    def __str__(self):
        return self.user.username

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    business_name = models.CharField(max_length=400, null=True)
    first_name = models.CharField(max_length=400, null=True)
    last_name = models.CharField(max_length=400, null=True)
    bank_name = models.CharField(max_length=400, null=True)
    bank_number = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    contact = models.CharField(max_length=20, null=True)
    alternate_contact = models.CharField(max_length=20, null=True, blank=True)
    category = models.CharField(max_length=400, choices=CATEGORIES, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.business_name}"