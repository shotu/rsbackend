# django_celery/celery.py

import os
from celery import Celery

from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rsbackend.settings.local")
app = Celery("rsbackend")
# app.config_from_object("django.conf:settings", namespace="CELERY")


app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Kolkata'  # Set the timezone to IST

# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     # 'add-every-monday-morning': {
#     #     'task': 'rsbackend.tasks.add',
#     #     # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
#     #     'schedule': 30,
#     #     'args': (16, 16),
#     # },
#     # 'download-scrip-masterdaily':{
#     #     'task': 'rsbackend.tasks.download_scrip_master',
#     #     # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
#     #     'schedule': 30,
#     #     'args': (),
#     # }
# }