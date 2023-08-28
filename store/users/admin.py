from django.contrib import admin

from products.admin import BucketAdmin
from users import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'image']
    inlines = BucketAdmin,


@admin.register(models.UserEmailVerification)
class EmailVerifAdmin(admin.ModelAdmin):
    list_display = 'code', 'user', 'expiration'
    fields = 'code', 'user', 'expiration', 'created_at'

    readonly_fields = 'created_at',
