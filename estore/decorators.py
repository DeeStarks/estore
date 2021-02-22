from django.shortcuts import redirect
from django.http import HttpResponse

# Redirects user back to the homepage if user is already logged in and tries to access the log in page
def authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store:index')
        return view_func(request, *args, **kwargs)
    return wrapper

# Switches user to his/her group when logged in - (Admin, Staff, Student)
def user_group(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            # Checking if the user belongs to a group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("<center><h4>YOU ARE NOT AUTHORIZED TO VIEW THIS PAGE. LET'S TAKE YOU BACK <a href='/'>HOME</a></h4></center>")
        return wrapper
    return decorator