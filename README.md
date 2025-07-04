Django WeatherBot API
A weather notification system built with Django REST Framework, Celery, Redis, and Telegram Bot integratiUsers can subscribe via Telegram to receive hourly and daily weather forecasts automatically.
Features
- Django REST API (DRF)
- Token-based Authentication
- Public and Protected Endpoints
- Celery + Redis for scheduled tasks
- Telegram Bot for real-time user interaction
- Environment-based config for production
- Clean code & commit history
Tech Stack
- Backend: Django, DRF
- Auth: DRF Token Authentication
- Asynchronous Tasks: Celery with Redis
- Bot: python-telegram-bot
- Scheduling: django-celery-beat
Setup Instructions
1. Clone the repository
 git clone https://github.com/vkrm03/WeatherApp.git
 cd WeatherApp
2. Create virtual environment
 python -m venv venv
 source venv/bin/activate (or venv\Scripts\activate on Windows)
3. Install dependencies
 pip install -r requirements.txt
4. Add .env file
 DEBUG=False
 SECRET_KEY=your_secret_key_here
 ALLOWED_HOSTS=127.0.0.1,localhost
 TELEGRAM_TOKEN=your_bot_token_here
 API_TOKEN=your_api_token_here
5. Migrate DB
 python manage.py migrate
6. Create superuser (for admin access)
 python manage.py createsuperuser
7. Start Redis server
Running the App
- Start Django server: python manage.py runserver
- Start Celery Worker: celery -A weather_app worker -l info
- Start Celery Beat: celery -A weather_app beat -l info
- Start the Telegram Bot: python bot.py
Authentication
- Token Authentication via DRF
- Register via Django admin or API
- Retrieve token using: POST /api/token/
API Endpoints
- Public: GET /api/current/
- Protected: GET /api/hourly/, /api/forecast/, POST /api/subscribe/
 (Use Authorization: Token your_api_token_here)
Telegram Bot Flow
- Start: /start
- Commands: /current_weather, /subscribe, /hourly, /forecast
- Prompts user for name, location, preferred times
- Forecasts delivered daily/hourly based on preferences
Testing
- Use Postman / curl for API
- Telegram app for bot interaction
Environment Variables
DEBUG, SECRET_KEY, ALLOWED_HOSTS, TELEGRAM_TOKEN, API_TOKEN

## Some of the Screenshots

![Subscription Step 1](imgs/Screenshot%202025-06-13%20120341.png)

![Subscription Step 2](imgs/Screenshot%202025-06-13%20120350.png)

![Forecast Preview](imgs/Screenshot%202025-06-13%20120524.png)
