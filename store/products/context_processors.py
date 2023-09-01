from django.http import HttpRequest

from products.models import Bucket


def buckets(request: HttpRequest):
    user = request.user
    return {'bucket': Bucket.objects.filter(user=user) if user.is_authenticated else []}
