from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UsersSerializer, ProductsSerializer, WishlistSerializer, CartSerializer, OrderSerializer, PendingOrderSerializer
from store.models import Product
from transactions.models import Wishlist, ShoppingCart, Order
from business.models import PendingOrder
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='account:signin')
@api_view(['GET'])
def users(request):
    users = User.objects.all().order_by('-id')
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)
    
@login_required(login_url='account:signin')
@api_view(['GET'])
def user(request, pk):
    user = User.objects.get(id=pk)
    serializer = UsersSerializer(user)
    return Response(serializer.data)

@login_required(login_url='account:signin')
@api_view(['GET'])
def products(request):
    products = Product.objects.all().order_by('-id')
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)
    
@login_required(login_url='account:signin')
@api_view(['GET', 'PUT'])
def product(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductsSerializer(product)
    if request.method == 'PUT':
        serializer = ProductsSerializer(instance=product,
        data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
    return Response(serializer.data)

@login_required(login_url='account:signin')
@api_view(['GET', 'POST'])
def wishlist(request, format=None):
    customer = User.objects.get(username=request.user)
    list = Wishlist.objects.filter(user=customer)
    serializer = WishlistSerializer(list, many=True)
    if request.method == 'POST':
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

    return Response(serializer.data)

@login_required(login_url='account:signin')
@api_view(['GET', 'DELETE'])
def wish_product(request, pk):
    customer = User.objects.get(username=request.user)
    product = Product.objects.get(id=pk)
    wish_product = Wishlist.objects.filter(user=customer).get(product=product)
    serializer = WishlistSerializer(wish_product)
    if request.method == 'DELETE':
        wish_product.delete()

    return Response(serializer.data)

@login_required(login_url='account:signin')
@api_view(['GET', 'POST'])
def cart(request, format=None):
    customer = User.objects.get(username=request.user)
    cart = ShoppingCart.objects.filter(user=customer)
    serializer = CartSerializer(cart, many=True)
    if request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

    return Response(serializer.data)

@login_required(login_url='account:signin')
@api_view(['GET', 'DELETE'])
def cart_product(request, pk):
    customer = User.objects.get(username=request.user)
    product = Product.objects.get(id=pk)
    cart_product = ShoppingCart.objects.filter(user=customer).get(product=product)
    serializer = CartSerializer(cart_product)
    if request.method == 'DELETE':
        cart_product.delete()

    return Response(serializer.data)
    
@login_required(login_url='account:signin')
@api_view(['GET', 'POST'])
def order(request, format=None):
    customer = User.objects.get(username=request.user)
    orders = Order.objects.filter(user=customer)
    serializer = OrderSerializer(orders, many=True)
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            for product in ShoppingCart.objects.filter(user=customer):
                product.delete()
        else:
            print(serializer.errors)
    return Response(serializer.data)
    
@login_required(login_url='account:signin')
@api_view(['GET', 'POST'])
def pending_orders(request):
    seller = User.objects.get(username=request.user)
    orders = PendingOrder.objects.filter(seller=seller)
    serializer = PendingOrderSerializer(orders, many=True)
    if request.method == 'POST':
        serializer = PendingOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
    return Response(serializer.data)