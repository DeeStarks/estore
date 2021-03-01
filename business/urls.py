from django.urls import path, include
from .views import shop, product_orders

app_name = 'business'

urlpatterns = [
    path("", shop, name="shop"),
    path("orders", product_orders, name="product_orders"),
]