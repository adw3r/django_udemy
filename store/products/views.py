from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    return render(request, 'products/index.html')


def products(request: HttpRequest):
    return render(request, 'products/products.html')
