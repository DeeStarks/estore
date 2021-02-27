from transactions.models import Wishlist, ShoppingCart
from django.contrib.auth.models import User
from store.models import ProductImage
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

def global_variable(request):
    review_ranges = {
        'zero': 0,
        'one': range(1, 21),
        'two': range(21, 41),
        'three': range(41, 61),
        'four': range(61, 81),
        'five': range(81, 101),
    }
    cart = None
    cart_product_ids = None
    wishlist = []
    wishlist_product_ids = []
    shipping_cost = 1000
    cart_sub_total = 0
    cart_grand_total = 0

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        cart = ShoppingCart.objects.filter(user=user)

        cart_product_ids = [cart.product.id for cart in ShoppingCart.objects.filter(user=user)]
        for product in cart:
            cart_sub_total += product.product.price
        cart_grand_total = cart_sub_total+shipping_cost

        for product in Wishlist.objects.filter(user=user):
            if product.product.id not in cart_product_ids and product.product.id not in wishlist_product_ids:
                wishlist_product_ids.append(product.product.id)
                
        for product in Wishlist.objects.filter(user=user):
            if product.product.id not in cart_product_ids and product.product.id not in [product.product.id for product in wishlist]:
                wishlist.append(product)

    return { 
        'review_ranges': review_ranges,
        'wishlist': wishlist,
        'wishlist_product_ids': wishlist_product_ids,
        'cart': cart,
        'cart_product_ids': cart_product_ids,
        'shipping_cost': shipping_cost,
        "cart_sub_total": cart_sub_total,
        "cart_grand_total": cart_grand_total
    }