from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todobackend.settings')

app = Celery('todotask', broker='redis://localhost:6379/0')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()