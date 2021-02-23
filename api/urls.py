from django.urls import path, include
from .views import products, product, wishlist, wish_product, users, user, cart, cart_product

app_name = 'api'

urlpatterns = [
    path('users', users, name="users"),
    path('user/<int:pk>', user, name="user"),
    path('products', products, name="products"),
    path('product/<int:pk>', product, name="product"),
    path('wishlist', wishlist, name="wishlist"),
    path('wishlist/product/<int:pk>', wish_product, name="wish_product"),
    path('cart', cart, name="cart"),
    path('cart/product/<int:pk>', cart_product, name="cart_product"),
]