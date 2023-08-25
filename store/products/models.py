from django.db import models

from users.models import User


class ProductCategory(models.Model):
    name: str = models.CharField(max_length=128, unique=True)
    description: str = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{type(self).__name__}(name={self.name!r})'


class Product(models.Model):
    title: str = models.CharField(max_length=256)
    description: str = models.TextField(null=True, blank=True)
    price: float = models.DecimalField(max_digits=6, decimal_places=2)
    qty: int = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='products_images')

    category: int = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{type(self).__name__}(title={self.title!r}, category={self.category})'


class BucketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(b.sum() for b in self)

    def total_qty(self):
        return sum(b.qty for b in self)


class Bucket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    qty: int = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = BucketQuerySet.as_manager()

    def __str__(self):
        return f'{type(self).__name__}(product={self.product}, user={self.user})'

    def sum(self):
        return self.product.price * self.qty
