import stripe
from django.conf import settings
from django.db import models
from users.models import User

stripe.api_key = settings.STRIPE_SECRET


class ProductCategory(models.Model):
    name: str = models.CharField(max_length=128, unique=True)
    description: str = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    def __str__(self):
        return f'{type(self).__name__}(name={self.name!r})'


class Product(models.Model):
    title: str = models.CharField(max_length=256)
    description: str = models.TextField(null=True, blank=True)
    price: float = models.DecimalField(max_digits=6, decimal_places=2)
    qty: int = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='products_images')
    stripe_price_id = models.CharField(max_length=128, null=True, blank=True)

    category: int = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{type(self).__name__}(title={self.title!r}, category={self.category})'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_price_id = stripe_product_price['id']
        super().save(force_insert, force_update, using, update_fields)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.title)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency="usd",
        )
        return stripe_product_price


class BucketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(b.sum() for b in self)

    def total_qty(self):
        return sum(b.qty for b in self)

    def get_line_items(self):
        line_items = [
            {
                'price': bucket.product.stripe_price_id,
                'quantity': bucket.qty,
            }
            for bucket in self
        ]
        return line_items


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

    def to_json(self):
        bucket_item = {
            'product_name': self.product.title,
            'quantity': self.qty,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return bucket_item
