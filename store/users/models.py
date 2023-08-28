from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified = models.BooleanField(default=False)


class UserEmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'{type(self).__name__} for user {self.user}'

    def send_verification_email(self):
        link = reverse(
            'users:email_verification', kwargs={
                'email': self.user.email,
                'code': self.code
            }
        )
        link = f'{settings.DOMAIN_NAME}{link}'
        send_mail(
            subject='Django store email verification email',
            message=f'Django store email verification link {link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email]
        )

    def is_expired(self) -> bool:
        return True if now() >= self.expiration else False
