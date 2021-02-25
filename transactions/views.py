from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ShoppingCart, Wishlist, Order, Checkout
from django.contrib.auth.models import User
from store.models import Product
from django.contrib.auth.decorators import login_required
from estore.decorators import user_group
import uuid

# Create your views here.
@login_required(login_url='account:signin')
def cart(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        price = request.POST.get('total')

        for product in Checkout.objects.filter(user=user):
            product.delete()
        
        order_products = {}
        order_uid = uuid.uuid4()
        for index, product_id in enumerate(product_ids):
            order_products[f'product{index+1}'] = {
                "product": Product.objects.get(id=product_id),
                "uuid": str(order_uid),
            }

        for index, quantity in enumerate(quantities):
            order_products[f'product{index+1}']['quantity'] = quantity

            order_products[f'product{index+1}']['price'] = int(order_products[f'product{index+1}']['product'].price) * int(quantity)

        for order in order_products:
            Checkout.objects.create(
                user=user,
                order_uid=order_uid,
                product=order_products[order]["product"],
                quantity=order_products[order]["quantity"],
                price=order_products[order]["price"],
            )
            
        return redirect(reverse('transaction:checkout', kwargs={"order_uid": order_uid}))
    return render(request, 'cart.html')
    
@login_required(login_url='account:signin')
def checkout(request, order_uid):
    user = User.objects.get(username=request.user)
    orders = Checkout.objects.filter(user=user).filter(order_uid=order_uid)
    price = 0
    shipping = 1000
    for order in orders:
        price += int(order.price)
    grand_price = price+shipping
    context = {
        "orders": orders,
        "shipping": shipping,
        "total_price": price,
        "grand_price": grand_price
    }
    return render(request, 'checkout.html', context)
    
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

@login_required(login_url='account:signin')
@user_group(allowed_roles=['seller'])
def shop(request):
    return render(request, 'shop.html')

@login_required(login_url='account:signin')
@user_group(allowed_roles=['customer'])
def sell(request):
    return render(request, 'sell.html')