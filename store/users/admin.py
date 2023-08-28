from django.contrib import admin
from products.admin import BucketAdmin
from users import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'image']
    inlines = BucketAdmin,
