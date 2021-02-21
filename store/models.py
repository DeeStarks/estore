from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORIES = (
    ("FASHION_BEAUTY", "Fashion & Beauty"),
    ("KIDS_CLOTHES", "Kids & Babies Clothes"),
    ("MEN_WOMEN_CLOTHES", "Men & Women Clothes"),
    ("GADGET_ACCESSORIES", "Gadgets & Accessories"),
    ("GADGET_ACCESSORIES", "Electronics & Accessories")
)
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, null=True)
    review_percentage = models.IntegerField(null=True, blank=True)
    sold = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='products/')
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product.product_name

class ProductSpecification(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True, null=True)
    detail = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.product.product_name

class ProductReview(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=150, blank=True, null=True)
    reviewer_email = models.EmailField(max_length=150, blank=True, null=True)
    review_text = models.CharField(max_length=1000, blank=True, null=True)
    review_rating = models.IntegerField(null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.reviewer_name} - {self.product.product_name}"


SUBSCRIPTION = (
    ('DAILY', 'One(1) Day - ₦1,000'),
    ('MONTHLY', 'One(1) Month - ₦25,000'),
    ('YEARLY', 'One(1) Year - ₦1,000'),
)

class ProductAdvert(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    banner = models.ImageField(blank=True, null=True, upload_to='advert_banners/')
    advert_description = models.CharField(max_length=200, blank=True, null=True)
    sub_duration = models.CharField(max_length=100, choices=SUBSCRIPTION, default='DAILY')

    def __str__(self):
        return self.product.product_name