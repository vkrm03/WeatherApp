from django.contrib import admin
from .models import Subscriber
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'chat_id', 'hourly_time', 'daily_time', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'chat_id', 'location')

