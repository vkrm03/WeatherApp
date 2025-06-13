import requests
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '7014027715:AAF8vOqDusiTj_UVivhwIYH7zSjE3v5CUB0'
API_TOKEN = '7959cc826b2fb87dbef5f111fc114ae6a2ce31ca'
API_BASE_URL = 'http://127.0.0.1:8000/api'

NAME, LOCATION, HOURLY_TIME, DAILY_TIME = range(4)
subscribed_users = set()

def generate_time_keyboard():
    times = [f"{str(h).zfill(2)}:00" for h in range(0, 24)]
    keyboard = [times[i:i+3] for i in range(0, len(times), 3)]
    return keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = [['/current_weather', '/subscribe']]
    await update.message.reply_text(
        "🌦️ Yo! Welcome to Django Weather Bot\nChoose an option below:",
        reply_markup=ReplyKeyboardMarkup(menu, one_time_keyboard=True, resize_keyboard=True)
    )

async def current_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {"Authorization": f"Token {API_TOKEN}"}
    try:
        response = requests.get(f"{API_BASE_URL}/current/", headers=headers)
        data = response.json()
        if response.status_code == 200:
            msg = (
                f"🌤️ Description: {data['description']}\n"
                f"🌡️ Temp: {data['temperature']}\n"
                f"💧 Humidity: {data['humidity']}\n"
                f"🌬️ Wind Speed: {data['wind_speed']}"
            )
        else:
            msg = "Failed to fetch weather data."
    except Exception as e:
        msg = f"Error: {str(e)}"
    await update.message.reply_text(msg)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What's your name?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Cool! Now drop your location name (city/town):")
    return LOCATION

async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location'] = update.message.text
    keyboard = generate_time_keyboard()
    await update.message.reply_text(
        "Select your preferred *Hourly Forecast* time:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return HOURLY_TIME

async def get_hourly_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['hourly_time'] = update.message.text
    keyboard = generate_time_keyboard()
    await update.message.reply_text(
        "Nice! Now select your *Daily Forecast* time:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return DAILY_TIME

async def get_daily_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['daily_time'] = update.message.text
    chat_id = update.effective_chat.id

    payload = {
        "name": context.user_data['name'],
        "location": context.user_data['location'],
        "chat_id": chat_id,
        "hourly_time": context.user_data['hourly_time'],
        "daily_time": context.user_data['daily_time']
    }
    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(f"{API_BASE_URL}/subscribe/", json=payload, headers=headers)
        if res.status_code in [200, 201]:
            subscribed_users.add(chat_id)
            await update.message.reply_text("You're subscribed! \nUse /hourly or /forecast anytime.")
        else:
            await update.message.reply_text("Failed to subscribe. Try again later.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Subscription cancelled.")
    return ConversationHandler.END

async def hourly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in subscribed_users:
        await update.message.reply_text("You need to /subscribe first!")
        return
    headers = {"Authorization": f"Token {API_TOKEN}"}
    try:
        res = requests.get(f"{API_BASE_URL}/hourly/", headers=headers)
        data = res.json()
        msg = "🌤Hourly Forecast (Next 18 hrs):\n"
        for item in data:
            msg += f"- {item['time']} | {item['description']} | {item['temperature']}\n"
    except Exception as e:
        msg = f"Error: {str(e)}"
    await update.message.reply_text(msg)

async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in subscribed_users:
        await update.message.reply_text("You need to /subscribe first!")
        return
    headers = {"Authorization": f"Token {API_TOKEN}"}
    try:
        res = requests.get(f"{API_BASE_URL}/forecast/", headers=headers)
        data = res.json()
        msg = "🌞 Daily Forecast:\n"
        for item in data:
            msg += f"- {item['date']} | {item['description']} | {item['temperature']}\n"
    except Exception as e:
        msg = f"Error: {str(e)}"
    await update.message.reply_text(msg)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type /start to begin.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("current_weather", current_weather))
    app.add_handler(CommandHandler("hourly", hourly))
    app.add_handler(CommandHandler("forecast", forecast))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("subscribe", subscribe)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            HOURLY_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_hourly_time)],
            DAILY_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_daily_time)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
