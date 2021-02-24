from django.contrib import admin
from .models import Wishlist, ShoppingCart, Order

# Register your models here.
admin.site.register(Wishlist)
admin.site.register(ShoppingCart)
admin.site.register(Order)
