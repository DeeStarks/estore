from django.urls import path, include
from .views import signup, signin, signout, account

app_name = 'account'

urlpatterns = [
    path('signup', signup, name="signup"),
    path('signin', signin, name="signin"),
    path('logout', signout, name="signout"),
    path('me/<str:username>', account, name="my_account"),
]