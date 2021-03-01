from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from estore.decorators import user_group
from .models import PendingOrder
from transactions.models import Order

# Create your views here.
@login_required(login_url='account:signin')
# @user_group(allowed_roles=['seller'])
def shop(request):
    context = {

    }
    return render(request, 'business/shop.html', context)

@login_required(login_url='account:signin')
# @user_group(allowed_roles=['seller'])
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
