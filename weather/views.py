import requests
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Subscriber
from .serializers import SubscriberSerializer

API_KEY = 'acbe2caff4a35bddeb1262a9a05eb28b'
LAT = '9.343255'
LON = '77.428030'

@api_view(['GET'])
@permission_classes([])
def get_current_weather(request):
    current_weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'
    response = requests.get(current_weather_url)
    data = response.json()

    if data["cod"] == 200:
        current_weather = {
            "description": data['weather'][0]['description'].capitalize(),
            "temperature": f"{data['main']['temp']}°C",
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} m/s"
        }
        return Response(current_weather)
    else:
        return Response({"error": "Failed to fetch weather data"}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hourly_weather(request):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data.get("cod") == "200":
        hourly_forecast = []

        for i in range(6):
            forecast = data['list'][i]
            hourly_forecast.append({
                "time": forecast['dt_txt'],
                "temperature": f"{forecast['main']['temp']}°C",
                "description": forecast['weather'][0]['description'],
                "icon": f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}@2x.png"
            })

        return Response(hourly_forecast)
    else:
        return Response({"error": "Failed to fetch hourly forecast"}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily_forecast(request):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data.get("cod") == "200":
        forecast_list = data['list']
        daily_forecast = []

        for i in range(0, len(forecast_list), 8):
            forecast = forecast_list[i]
            daily_forecast.append({
                "date": forecast['dt_txt'].split()[0],
                "temperature": f"{forecast['main']['temp']}°C",
                "description": forecast['weather'][0]['description'],
                "icon": f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}@2x.png"
            })

        return Response(daily_forecast)
    else:
        return Response({"error": "Failed to fetch forecast"}, status=500)




@api_view(['POST'])
@permission_classes([])
def subscribe_user(request):
    print(request.data)
    name = request.data.get("name")
    location = request.data.get("location")
    chat_id = request.data.get("chat_id")
    hourly_time = request.data.get("hourly_time")
    daily_time = request.data.get("daily_time")

    if not all([name, location, chat_id]):
        return Response({"error": "Missing required fields"}, status=400)

    try:
        subscriber, created = Subscriber.objects.get_or_create(chat_id=chat_id)
        subscriber.name = name
        subscriber.location = location
        subscriber.hourly_time = hourly_time
        subscriber.daily_time = daily_time
        subscriber.is_active = True
        subscriber.save()

        return Response({"message": "Subscribed successfully"}, status=201 if created else 200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
