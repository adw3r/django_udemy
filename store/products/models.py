from django.db import models


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
