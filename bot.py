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

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token & API Config
TOKEN = '7014027715:AAF8vOqDusiTj_UVivhwIYH7zSjE3v5CUB0'
API_TOKEN = '7959cc826b2fb87dbef5f111fc114ae6a2ce31ca'
API_BASE_URL = 'http://127.0.0.1:8000/api'

# Subscription states
NAME, LOCATION = range(2)
subscribed_users = set()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = [['/current_weather', '/subscribe']]
    await update.message.reply_text(
        "🌦️ Yo! Welcome to Django Weather Bot\nChoose an option below:",
        reply_markup=ReplyKeyboardMarkup(menu, one_time_keyboard=True, resize_keyboard=True)
    )

# /current_weather (Public)
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

# /subscribe flow - Step 1
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What's your name?")
    return NAME

# /subscribe flow - Step 2
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Cool! Now drop your location name (city/town):")
    return LOCATION

# /subscribe flow - Step 3
async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data['name']
    location = update.message.text
    chat_id = update.effective_chat.id

    payload = {
        "name": name,
        "location": location,
        "chat_id": chat_id,
    }
    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(f"{API_BASE_URL}/subscribe/", json=payload, headers=headers)
        if res.status_code in [200, 201]:
            subscribed_users.add(chat_id)
            await update.message.reply_text("You're subscribed! Use /hourly or /forecast now.")
        else:
            await update.message.reply_text("Failed to subscribe. Try again later.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
    return ConversationHandler.END

# Cancel subscription flow
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Subscription cancelled.")
    return ConversationHandler.END

# Hourly forecast (private)
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

# Daily forecast (private)
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

# Echo handler for unknown text
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type /start to begin.")

# Main function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("current_weather", current_weather))
    app.add_handler(CommandHandler("hourly", hourly))
    app.add_handler(CommandHandler("forecast", forecast))

    # Conversation handler for /subscribe
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("subscribe", subscribe)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)

    # Default text response
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
