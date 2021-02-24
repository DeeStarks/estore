from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=100, null=True)
    permanent_address = models.CharField(max_length=400, null=True)
    shipping_address = models.CharField(max_length=400, null=True)