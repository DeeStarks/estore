from django.contrib import admin
from .models import Wishlist, ShoppingCart, Order, Checkout

# Register your models here.
admin.site.register(Wishlist)
admin.site.register(ShoppingCart)
admin.site.register(Order)
admin.site.register(Checkout)
