from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Bucket

stripe.api_key = settings.STRIPE_SECRET


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context = {
            'title': f'Order #{self.object.id}'
        }

        context_data.update(context)
        return context_data


class OrderListView(TitleMixin, ListView):
    queryset = Order.objects.all()
    # model = Order
    title = 'My Orders'
    template_name = 'orders/orders.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Success'


class CancelTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'
    title = 'Order canceled'


class OrderCreateView(TitleMixin, CreateView):
    title = 'Order processing'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        buckets = Bucket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=buckets.get_line_items(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=f'{settings.DOMAIN_NAME}{reverse("orders:success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse("orders:cancel")}',
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )
        # line_items = session.line_items
        fulfill_order(session)
    return HttpResponse(status=200)


def fulfill_order(session):
    # TODO: fill me in
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
    print("Fulfilling order")
