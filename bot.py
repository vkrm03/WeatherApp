import asyncio
import requests
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '7014027715:AAF8vOqDusiTj_UVivhwIYH7zSjE3v5CUB0'
API_URL = 'http://127.0.0.1:8000/api/current/'
API_TOKEN = '7959cc826b2fb87dbef5f111fc114ae6a2ce31ca'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /start from %s", update.effective_user.first_name)
    menu = [['/current_weather', '/subscribe']]
    await update.message.reply_text(
        "🌦️ Yo! Welcome to Django Weather Bot\nChoose an option below:",
        reply_markup=ReplyKeyboardMarkup(menu, one_time_keyboard=True, resize_keyboard=True)
    )

async def current_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /current_weather from %s", update.effective_user.first_name)
    headers = {"Authorization": f"Token {API_TOKEN}"}
    try:
        response = requests.get(API_URL, headers=headers)
        data = response.json()

        if response.status_code == 200:
            weather_info = (
                f"🌤️ Description: {data['description']}\n"
                f"🌡️ Temp: {data['temperature']}\n"
                f"💧 Humidity: {data['humidity']}\n"
                f"🌬️ Wind Speed: {data['wind_speed']}"
            )
        else:
            weather_info = "⚠Failed to fetch weather data."

    except Exception as e:
        weather_info = f"Error: {str(e)}"

    await update.message.reply_text(weather_info)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /subscribe from %s", update.effective_user.first_name)
    await update.message.reply_text("📝 Subscribing you! (Feature coming soon...)")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received message: %s", update.message.text)
    await update.message.reply_text("Echo: " + update.message.text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("current_weather", current_weather))
    app.add_handler(CommandHandler("subscribe", subscribe))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
