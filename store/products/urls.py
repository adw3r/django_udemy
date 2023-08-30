from django.urls import path

from products.views import ProductsListView, bucket_add, bucket_remove

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('buckets/add/<int:product_id>/', bucket_add, name='bucket_add'),
    path('buckets/remove/<int:bucket_id>/', bucket_remove, name='bucket_remove'),
]
