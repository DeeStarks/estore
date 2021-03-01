from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.
class PendingOrder(models.Model):
    seller = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='seller')
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='customer')
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    order_uid = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField(null=True)
    total_price = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.seller.username} - {self.product.product_name}"