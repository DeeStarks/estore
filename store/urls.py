from django.urls import path, include
from .views import index, products, product_detail

app_name = 'store'

urlpatterns = [
    path('', index, name="index"),
    path('products', products, name="product_list"),
    path('product/<int:product_id>/<str:title>', product_detail, name='product_detail')
]