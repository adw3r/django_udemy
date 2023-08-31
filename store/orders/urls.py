from django.urls import path
from orders.views import (CancelTemplateView, OrderCreateView, OrderDetailView,
                          OrderListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='index'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('success/', SuccessTemplateView.as_view(), name='success'),
    path('cancel/', CancelTemplateView.as_view(), name='cancel'),
]
