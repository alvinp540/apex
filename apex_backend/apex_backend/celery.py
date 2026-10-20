import os
from celery import Celery

default_settings = (
    'apex_backend.settings.production'
    if os.environ.get('VERCEL')
    else 'apex_backend.settings.development'
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', default_settings)

app = Celery('apex_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
