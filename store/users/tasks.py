import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now
from users.models import UserEmailVerification, User

EMAIL_VERIF_EXPIRATION_LIMIT = 60


@shared_task
def send_email_verif(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(minutes=EMAIL_VERIF_EXPIRATION_LIMIT)
    print(expiration)
    record = UserEmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    print(record)
    record.send_verification_email()
