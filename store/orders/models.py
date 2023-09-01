from django.db import models

from products.models import Bucket
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name: str = models.CharField(max_length=64)
    last_name: str = models.CharField(max_length=64)
    email: str = models.EmailField(max_length=256)
    address: str = models.CharField(max_length=256)
    bucket_history = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{type(self).__name__}(id={self.id}, status={self.status}, user={self.user})'

    def update_after_payment(self):
        buckets = Bucket.objects.filter(user=self.user)
        self.status = self.PAID
        self.bucket_history = {
            'purchased_items': [b.to_json() for b in buckets],
            'total_sum': float(buckets.total_sum()),
        }

        buckets.delete()
        self.save()
