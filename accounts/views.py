from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from estore.decorators import authenticated_user, user_group
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from transactions.models import Order
from .models import Profile

# Create your views here.
@authenticated_user
def signup(request):
    error = {
        'email': '',
        'username': '',
        'password': ''
    }
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if email not in [user.email for user in User.objects.all()]:
            if username not in [user.username for user in User.objects.all()]:
                if password1 == password2:
                    User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        username=username,
                        password=password1
                    )
                    group = Group.objects.update_or_create(
                        name='customer',
                        defaults={
                            'name': 'customer'
                        }
                    )
                    user = User.objects.get(username=username)
                    user.groups.add(group)
                    update_session_auth_hash(request, user)
                    return redirect('account:signin')
                else:
                    error['password'] = "Password did not match"
            else:
                error['username'] = "Username already exist"
        else:
            error['email'] = "User with this email already exist"

    context = {
        'error': error
    }
    return render(request, 'signup.html', context)

@authenticated_user
def signin(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('store:index')
            else:
                error = "Username or password incorrect"
                print('password')
        except ObjectDoesNotExist:
            error = "Username or password incorrect"
            print("username")
    context = {
        'error': error
    }
    return render(request, 'login.html', context)

def signout(request):
    logout(request)
    return redirect('account:signin')
    
@login_required(login_url='account:signin')
def account(request, username):
    user = User.objects.get(username=request.user)
    orders = Order.objects.filter(user=user)
    user_details = None
    try:
        profile = Profile.objects.get(user=user)
        user_details = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "mobile": profile.mobile,
            "permanent_address": profile.permanent_address,
            "shipping_address": profile.shipping_address
        }
    except ObjectDoesNotExist:
        user_details = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }

    if request.method == 'POST' and 'update_account' in request.POST:
        pass
    elif request.method == 'POST' and 'change_password' in request.POST:
        pass
    context = {
        'orders': orders,
        'profile': user_details
    }
    return render(request, 'my-account.html', context)