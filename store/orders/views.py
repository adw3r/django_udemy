from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from orders.forms import OrderForm

from common.views import TitleMixin


class OrderCreateView(TitleMixin, CreateView):
    title = 'Order processing'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OrderView(TemplateView):
    template_name = 'orders/order.html'
