from django.contrib import admin
from .models import Product, ProductImage, ProductSpecification, ProductReview, ProductAdvert, ClothSize

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSpecification)
admin.site.register(ProductReview)
admin.site.register(ProductAdvert)
admin.site.register(ClothSize)