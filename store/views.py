from django.shortcuts import render
import random
from django.contrib.auth.models import User
from .models import Product, ProductImage, ProductSpecification, ProductReview, ProductAdvert
from transactions.models import Wishlist, ShoppingCart
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    all_products = Product.objects.all()
    featured_products = []
    recent_products = all_products.order_by("-id")[:10]
    adverts = []

    # To be displayed featured products
    all_featured = [product for product in all_products if product.featured]
    if all_featured:
        for count in range(10):
            product = random.choice(all_featured)
            if product not in featured_products:
                featured_products.append(product)

    # To be displayed adverts
    all_adverts = [product for product in ProductAdvert.objects.all()]
    if all_adverts:
        for count in range(10):
            product = random.choice(all_adverts)
            if product not in adverts:
                adverts.append(product)

    context = {
        'products': [product for product in all_products],
        'featured': featured_products,
        'adverts': adverts,
        'recent': recent_products,
        'product_images': ProductImage,
    }
    return render(request, 'index.html', context)

def products(request):
    search_length = 0
    search_value = None
    paginator = Paginator(Product.objects.all().order_by('-id'), 10)
    products = paginator.page(1)

    if 'search' in request.GET:
        search_value = request.GET.get('search')
        query = Product.objects.filter(product_name__icontains=search_value).order_by('-id')
        paginator = Paginator(query, 10)
        products = paginator.page(1)
        search_length = query.count()

    if 'page' in request.GET:
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

    # Price ranges 
    highest_price = 0
    for product in Product.objects.all():
        if product.price > highest_price:
            highest_price = product.price
    price_ranges = [[0, 1000]]
    previous_range = 1000
    for i in range(int(highest_price+1)):
        if i % 1000 == 0 and i not in [0, 1000]:
            price_ranges.append([previous_range, i])
            previous_range += 1000

    return render(request, 'product-list.html', {
        'products': products,
        'search_length': search_length,
        'search_value': search_value,
        'price_ranges': price_ranges
    })

def product_detail(request, product_id, title):
    product = Product.objects.get(id=product_id)
    related = []
    other_products = []
    for product__obj in Product.objects.all():
        for product_obj_word in product__obj.product_name.split(" "):
            for product_word in product.product_name.split(" "):
                if product_obj_word not in ['is', 'are', 'for', 'in', 'that', 'or'] and product_obj_word == product_word and product__obj != product and product__obj not in related:
                    related.append(product__obj) 
    
    user_products = [product for product in Product.objects.filter(seller=product.seller)]
    if user_products:
        for count in range(10):
            product__obj = random.choice(user_products)
            if product__obj not in other_products and product__obj != product:
                other_products.append(product__obj)

    if request.method == 'POST':
        rate = request.POST.get('reviewer_rate')
        name = request.POST.get('reviewer_name')
        email = request.POST.get('reviewer_email')
        text = request.POST.get('reviewer_text')
        percentage_rate = 0
        if rate:
            percentage_rate = int((int(rate)/5)*100)
            
        total_rate = int(((percentage_rate+product.rating)/200)*100)
        product.rating = total_rate
        product.save()

        ProductReview.objects.create(
            product=product,
            seller=product.seller,
            reviewer_name=name,
            reviewer_email=email,
            review_rating=percentage_rate,
            review_text=text
        )

    context = {
        "product": product,
        'related_products': related,
        'other_products': other_products
    }
    return render(request, 'product-detail.html', context)