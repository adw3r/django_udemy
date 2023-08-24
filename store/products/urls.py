from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from products.views import products

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
]
