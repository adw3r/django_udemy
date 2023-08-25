from django.http import HttpRequest
from django.shortcuts import render
from products.models import ProductCategory, Product


def index(request: HttpRequest):
    context = {
        'title': 'Django store',
        'username': 'wezxasqw',
        'is_flagged': True
    }
    return render(request, 'products/index.html', context=context)


def products(request: HttpRequest):
    context = {
        'title': 'My products',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'products/products.html', context=context)
