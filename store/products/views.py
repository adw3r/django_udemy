from common.views import TitleMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from products.models import Bucket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Django store'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'username': self.request.user.username,
                'is_flagged': True
            }
        )
        return context


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'My products'

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()

        context = {
            'categories': ProductCategory.objects.all()
        }
        context_data.update(context)
        return context_data


@login_required
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


@login_required
def bucket_remove(request, bucket_id):
    bucket = Bucket.objects.get(id=bucket_id)
    bucket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
