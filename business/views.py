from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from estore.decorators import user_group
from .models import PendingOrder
from transactions.models import Order
from store.models import Product, SIZES, SUBSCRIPTION, ProductAdvert, ClothSize, ProductImage, ProductSpecification
from accounts.models import BusinessProfile
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='account:signin')
@user_group(allowed_roles=['seller'])
def shop(request):
    seller = User.objects.get(username=request.user)
    products = Product.objects.filter(seller=seller)
    context = {
        "products": products
    }
    return render(request, 'business/shop.html', context)

@login_required(login_url='account:signin')
@user_group(allowed_roles=['seller'])
def add_product(request):
    business_profile = BusinessProfile.objects.get(user=request.user)
    subscriptions = []
    for sub in SUBSCRIPTION:
        subscriptions.append([sub[1].split("₦")[1].replace(",", ""), sub[1], sub[0]])
        
    if request.method == 'POST':
        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        discount = request.POST.get("discount")
        spec_title = request.POST.getlist("spec_title")
        spec_detail = request.POST.getlist("spec_detail")
        sub_type = request.POST.get("sub_type")
        shipped = False
        featured = False
        specification = []
        sizes = []
        images = []
        if request.POST.get("shipped") == 'True':
            shipped = True
        if sub_type:
            featured = True
        for index in range(len(spec_title)):
            specification.append([spec_title[index], spec_detail[index]])

        if request.POST.getlist("sizes"):
            sizes = request.POST.getlist("sizes")

        if request.FILES:
            images = request.FILES.getlist("images")
        
        # Creating the product
        product = Product.objects.create(
            seller=request.user,
            product_name=product_name,
            description=description,
            original_price=int(price),
            discount=int(discount),
            price=int(price)-int(discount),
            category=business_profile.category,
            featured=featured,
            shipped=shipped
        )

        # Adding cloth's sizes
        for size in sizes:
            ClothSize.objects.create(
                product=product,
                size=size
            )

        # Adding its specifications
        for spec in specification:
            ProductSpecification.objects.create(
                product=product,
                title=spec[0],
                detail=spec[1]
            )
        
        # Adding its images
        for index in range(len(images)):
            if index == 0:
                ProductImage.objects.create(
                    product=product,
                    image=images[index],
                    default=True
                )
            else:
                ProductImage.objects.create(
                    product=product,
                    image=images[index],
                    default=False
                )
        return redirect(reverse('business:finalize_product_addition', kwargs={
            "id": product.id,
            "sub_type": sub_type.lower()
        }))
    context = {
        "sizes": SIZES,
        "subscriptions": subscriptions,
        "seller_category": business_profile.get_category_display(),
        "paystack_pubkey": settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request, 'business/add_product.html', context)

@login_required(login_url='account:signin')
# @user_group(allowed_roles=['seller'])
def finalize_product_addition(request, id, sub_type):
    try:
        product = Product.objects.filter(seller=request.user).get(id=id)
        images = ProductImage.objects.filter(product=product)
        if request.method == 'POST':
            for image in ProductImage.objects.filter(product=product):
                image.default = False
                image.save()

            default = request.POST.get("image")
            default_image = ProductImage.objects.get(id=int(default))
            default_image.default = True
            default_image.save()

            if request.FILES:
                banner = request.FILES.get("banner")
                ProductAdvert.objects.create(
                    seller=request.user,
                    product=product,
                    advert_title=product.product_name,
                    advert_description=product.description,
                    sub_duration=sub_type.upper(),
                    banner=banner
                )
            return redirect('store:index')

        context = {
            "product_is_featured": product.featured,
            "images": images
        }
        return render(request, 'business/finalize_product_add.html', context)
    except ObjectDoesNotExist:
        return HttpResponse("<center><h4>YOU ARE NOT AUTHORIZED TO VIEW THIS PAGE. LET'S TAKE YOU BACK <a href='/'>HOME</a></h4></center>")

@login_required(login_url='account:signin')
@user_group(allowed_roles=['seller'])
def product_orders(request):
    user = User.objects.get(username=request.user)
    pending_orders = PendingOrder.objects.filter(seller=user)

    # Approving orders
    if 'approve' in request.POST:
        order_id = request.POST.get("approve")
        if int(order_id) in [order.id for order in pending_orders]:
            pending_order = pending_orders.get(id=order_id)
            order = Order.objects.filter(user=pending_order.customer).get(order_uid=pending_order.order_uid)
            order.status = "APPROVED"
            order.save()
            pending_order.delete()
            pending_orders = PendingOrder.objects.filter(seller=user)
    elif 'approve_all' in request.POST:
        for order in pending_orders:
            pending_order = pending_orders.get(id=order.id)
            order = Order.objects.filter(user=pending_order.customer).get(order_uid=pending_order.order_uid)
            order.status = "APPROVED"
            order.save()
            pending_order.delete()
            pending_orders = PendingOrder.objects.filter(seller=user)

    context = {
        "pending_orders": pending_orders
    }
    return render(request, 'business/product_orders.html', context)
