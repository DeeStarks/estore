from rest_framework import serializers
from django.contrib.auth.models import User
from store.models import Product
from transactions.models import Wishlist, ShoppingCart, Order
from business.models import PendingOrder


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PendingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingOrder
        fields = '__all__'