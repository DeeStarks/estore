from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ShoppingCart
from django.contrib.auth.models import User
from store.models import Product

# Create your views here.
def cart(request):
    context = {
        
    }
    return render(request, 'cart.html', context)
    
def add_to_cart(request, pk):
    user = User.objects.get(username=request.user)
    product = Product.objects.get(id=pk)
    cart = ShoppingCart.objects.filter(user=user)
    if product not in [product.product for product in cart]:
        ShoppingCart.objects.create(
            user=user,
            product=product
        )
    return redirect('transaction:cart')
    
def remove_from_cart(request, pk):
    user = User.objects.get(username=request.user)
    ShoppingCart.objects.filter(user=user).get(id=pk).delete()
    return redirect('transaction:cart')
