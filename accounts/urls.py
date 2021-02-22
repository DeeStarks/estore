from django.urls import path, include
from .views import signup, signin, signout

app_name = 'account'

urlpatterns = [
    path('signup', signup, name="signup"),
    path('signin', signin, name="signin"),
    path('logout', signout, name="signout"),
]