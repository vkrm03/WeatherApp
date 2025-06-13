from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_app.settings')

app = Celery('weather_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
