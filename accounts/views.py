from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from estore.decorators import authenticated_user, user_group
from django.contrib.auth import login, logout

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