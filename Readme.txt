Django Internship Assignment Task:

You are required to build a small Django project that demonstrates your backend development skills. The assignment includes Django REST Framework,
authentication, Celery, Telegram bot integration, and proper code management.


Requirements:

1 Django Project Setup
Create a Django project using Django Rest Framework (DRF).
Setup proper settings.py for production:
Set DEBUG=False .
Use environment variables for secrets (e.g. secret key, DB credentials, API keys).

2 API Development
Create at least 2 API endpoints:
Public endpoint (accessible to everyone).
Protected endpoint (accessible only to authenticated users using TokenAuth or JWT).
Implement Django Login for web-based access.

3 Celery Integration
Setup Celery with Redis as the broker.
Implement one background task (example: send email after user registration).

4 Telegram Bot Integration
Create a Telegram Bot using Telegram Bot API.
When users send a /start command to the bot, collect their Telegram username and store it into your Django databa