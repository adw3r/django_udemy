from django.contrib import admin

from products import models

admin.site.register(models.ProductCategory)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'title', 'price', 'qty', 'category', 'stripe_price_id'
    fields = 'title', 'description', ('price', 'qty'), 'img'
    # readonly_fields = ['description']
    search_fields = ['title']
    # ordering = ['title', 'qty']


class BucketAdmin(admin.TabularInline):
    model = models.Bucket
    fields = 'product', 'qty', 'created_at'
    readonly_fields = 'created_at',
    extra = 0
