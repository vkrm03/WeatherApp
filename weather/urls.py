from django.urls import path
from . import views
from .views import subscribe_user

urlpatterns = [
    path('current/', views.get_current_weather),
    path('hourly/', views.get_hourly_weather),
    path('forecast/', views.get_daily_forecast),
    path('subscribe/', subscribe_user, name='subscribe_user'),
]
