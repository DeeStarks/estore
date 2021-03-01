from django.urls import path, include
from .views import cart, verify, add_to_cart, remove_from_cart, wishlist, remove_from_wishlist, shop, sell, checkout

app_name = 'transaction'

urlpatterns = [
    path('cart', cart, name="cart"),
    path('verify/<str:ref_id>', verify, name="verify"),
    path('cart/add/<int:pk>', add_to_cart, name="add_to_cart"),
    path('cart/remove/<int:pk>', remove_from_cart, name="remove_from_cart"),
    path('wishlist', wishlist, name='wishlist'),
    path('wishlist/remove/<int:pk>', remove_from_wishlist, name="remove_from_wishlist"),
    path('checkout/<str:order_uid>', checkout, name="checkout"),
    path('shop', shop, name="shop"),
    path('sell', sell, name='sell')
]