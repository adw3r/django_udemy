import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

app = Celery('store', broker=settings.REDIS_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
