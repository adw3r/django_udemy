import os

from django.conf import settings

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

app = Celery('store', broker=settings.REDIS_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
