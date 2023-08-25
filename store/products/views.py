from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from products.models import ProductCategory, Product, Bucket


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


def bucket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    buckets = Bucket.objects.filter(user=request.user, product=product)

    if not buckets.exists():
        Bucket.objects.create(user=request.user, product=product, qty=1)
    else:
        bucket = buckets.first()
        bucket.qty += 1
        bucket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # return HttpResponseRedirect(request.path)


def bucket_remove(request, bucket_id):
    bucket = Bucket.objects.get(id=bucket_id)
    bucket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
