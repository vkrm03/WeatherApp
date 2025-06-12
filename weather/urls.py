from django.urls import path
from . import views

urlpatterns = [
    path('current/', views.get_current_weather),
    path('hourly/', views.get_hourly_weather),
    path('forecast/', views.get_daily_forecast),
]
