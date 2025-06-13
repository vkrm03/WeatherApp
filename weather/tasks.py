from celery import shared_task
from .models import Subscriber
import requests
from datetime import datetime

TELEGRAM_TOKEN = '7014027715:AAF8vOqDusiTj_UVivhwIYH7zSjE3v5CUB0'
API_TOKEN = '7959cc826b2fb87dbef5f111fc114ae6a2ce31ca'
API_BASE_URL = 'http://127.0.0.1:8000/api'


def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    response = requests.post(url, json={"chat_id": chat_id, "text": text})
    print(f"Sent message to {chat_id}: {response.status_code} | {response.text}")


@shared_task
def send_scheduled_weather():
    now = datetime.now().time()
    print(f"[{datetime.now()}] Running scheduled weather task")

    users = Subscriber.objects.filter(is_active=True)
    print(f"Found {users.count()} active users")

    for user in users:
        print(f"Processing user: {user.name} | Chat ID: {user.chat_id}")

        if user.hourly_time:
            print(f"User hourly time: {user.hourly_time.hour} | Current hour: {now.hour}")
            if now.hour == user.hourly_time.hour:
                print("Matched hourly time. Sending hourly forecast...")
                response = requests.get(
                    f"{API_BASE_URL}/hourly/",
                    headers={"Authorization": f"Token {API_TOKEN}"}
                )
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            msg = "🌤️ Hourly Forecast:\n"
                            for item in data[:6]:
                                msg += f"{item['time']} - {item['description']} - {item['temperature']}\n"
                            send_message(user.chat_id, msg)
                        else:
                            print("Expected list for hourly forecast, got:", data)
                    except Exception as e:
                        print("Error parsing hourly forecast:", e)
                else:
                    print("Failed to fetch hourly forecast:", response.status_code, response.text)
            else:
                print("Current hour doesn't match hourly time.")

        if user.daily_time:
            print(f"User daily time: {user.daily_time.hour} | Current hour: {now.hour}")
            if now.hour == user.daily_time.hour:
                print("Matched daily time. Sending daily forecast...")
                response = requests.get(
                    f"{API_BASE_URL}/forecast/",
                    headers={"Authorization": f"Token {API_TOKEN}"}
                )
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            msg = "🌞 Daily Forecast:\n"
                            for item in data:
                                msg += f"{item['date']} - {item['description']} - {item['temperature']}\n"
                            send_message(user.chat_id, msg)
                        else:
                            print("Expected list for daily forecast, got:", data)
                    except Exception as e:
                        print("Error parsing daily forecast:", e)
                else:
                    print("Failed to fetch daily forecast:", response.status_code, response.text)
            else:
                print("Current hour doesn't match daily time.")
