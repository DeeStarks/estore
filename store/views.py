from django.shortcuts import render
import random
from .models import Product, ProductImage, ProductSpecification, ProductReview, ProductAdvert

# Create your views here.
def index(request):
    all_products = Product.objects.all()
    featured_products = []
    all_featured = []
    for product in all_products:
        if product.is_featured:
            all_featured.append(product)
    
    # featured_products = random.choices(all_featured, k=10)
    if all_featured:
        for count in range(10):
            product = random.choice(all_featured)
            if product not in featured_products:
                featured_products.append(product)

    return render(request, 'index.html')