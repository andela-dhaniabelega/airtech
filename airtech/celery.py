from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airtech.settings')
app = Celery('airtech')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered apps
app.autodiscover_tasks()