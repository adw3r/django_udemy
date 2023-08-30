from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from orders.forms import OrderForm


# Create your views here.
class OrderView(TemplateView):
    template_name = 'orders/order.html'


# Create your views here.
class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
