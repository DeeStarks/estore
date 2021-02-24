from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ShoppingCart, Wishlist
from django.contrib.auth.models import User
from store.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.
class CartShop:
    def __init__(self):
        self.products = None
        self.quantities = None
        self.price = None

    @login_required(login_url='account:signin')
    @classmethod
    def cart(request, cls):
        if request.method == 'POST':
            self.products = request.POST.getlist('product')
            self.quantities = request.POST.getlist('quantity')
            self.price = request.POST.get('total')
            print(f'''
Products = {[Product.objects.get(id=product) for product in self.products]}
Quantities = {self.quantities}
Price = {self.price}        
            ''')
        return render(request, 'cart.html')
        
@login_required(login_url='account:signin')
def add_to_cart(request, pk):
    user = User.objects.get(username=request.user)
    product = Product.objects.get(id=pk)
    cart = ShoppingCart.objects.filter(user=user)
    if product not in [product.product for product in cart]:
        ShoppingCart.objects.create(
            user=user,
            product=product
        )
    if product.id in [product.product.id for product in Wishlist.objects.filter(user=user)]:
        wishlist_product = Product.objects.get(id=product.id)
        Wishlist.objects.filter(user=user).get(product=wishlist_product).delete()
    return redirect('transaction:cart')
    
@login_required(login_url='account:signin')
def remove_from_cart(request, pk):
    user = User.objects.get(username=request.user)
    ShoppingCart.objects.filter(user=user).get(id=pk).delete()
    return redirect('transaction:cart')

@login_required(login_url='account:signin')
def wishlist(request):
    return render(request, 'wishlist.html')
    
@login_required(login_url='account:signin')
def remove_from_wishlist(request, pk):
    user = User.objects.get(username=request.user)
    wishlist.objects.filter(user=user).get(id=pk).delete()
    return redirect('transaction:wishlist')