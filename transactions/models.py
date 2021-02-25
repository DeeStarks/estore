from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.product.product_name

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.product_name

STATUS = (
    ("PENDING", "Pending"),
    ("APPROVED", "Approved")
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_uid = models.CharField(max_length=200, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    order_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.order_uid}"

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_uid = models.CharField(max_length=200, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.order_uid}"
