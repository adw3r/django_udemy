# Generated by Django 3.2.15 on 2023-08-31 12:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0005_product_stripe_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stripe_price',
            new_name='stripe_price_id',
        ),
    ]