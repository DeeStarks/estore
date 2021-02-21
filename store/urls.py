from django.urls import path, include
from .views import index

app_name = 'store'

urlpatterns = [
    path('', index, name="index"),
]