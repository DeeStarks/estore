from django.urls import path, include
from .views import shop, product_orders, add_product, finalize_product_addition

app_name = 'business'

urlpatterns = [
    path("", shop, name="shop"),
    path("orders", product_orders, name="product_orders"),
    path("add", add_product, name="add_product"),
    path("add/finalize/<int:id>/<str:sub_type>", finalize_product_addition, name="finalize_product_addition"),
]