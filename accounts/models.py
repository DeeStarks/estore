from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mobile = PhoneNumberField(null=True, blank=True, unique=True)
    permanent_address = models.CharField(max_length=400, null=True)
    shipping_address = models.CharField(max_length=400, null=True)

    def __str__(self):
        return self.user.username