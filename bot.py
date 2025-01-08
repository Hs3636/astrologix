# import os
# from dotenv import load_dotenv
# import telebot
# import requests
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# # Load environment variables
# load_dotenv()
# BOT_TOKEN = os.getenv('BOT_TOKEN')

# # Validate BOT_TOKEN
# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN is not set!")

# bot = telebot.TeleBot(BOT_TOKEN)

# def get_daily_horoscope(sign: str, day: str) -> dict:
#     """Get daily horoscope for a zodiac sign."""
#     url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
#     params = {"sign": sign, "day": day}
#     response = requests.get(url, params)
#     return response.json()

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, "Enter /horoscope to start")

# @bot.message_handler(commands=['horoscope'])
# def sign_handler(message):
#     # Create an inline keyboard for zodiac signs
#     keyboard = InlineKeyboardMarkup()
#     zodiac_signs = [
#         "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
#         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
#     ]
#     for sign in zodiac_signs:
#         keyboard.add(InlineKeyboardButton(sign, callback_data=f"sign_{sign}"))
    
#     text = "Choose your zodiac sign:"
#     bot.send_message(message.chat.id, text, reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: call.data.startswith("sign_"))
# def day_handler(call):
#     sign = call.data.split("_")[1]
#     # Create an inline keyboard for days
#     keyboard = InlineKeyboardMarkup()
#     days = ["TODAY", "TOMORROW", "YESTERDAY"]
#     for day in days:
#         keyboard.add(InlineKeyboardButton(day, callback_data=f"day_{sign}_{day}"))
    
#     text = f"You selected *{sign}*.\nNow choose a day:"
#     bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
# def fetch_horoscope(call):
#     _, sign, day = call.data.split("_")
#     horoscope = get_daily_horoscope(sign, day)
#     data = horoscope["data"]
#     horoscope_message = (
#         f'*Horoscope:* {data["horoscope_data"]}\n'
#         f'*Sign:* {sign}\n'
#         f'*Day:* {data["date"]}'
#     )
#     bot.send_message(call.message.chat.id, "Here's your horoscope!")
#     bot.send_message(call.message.chat.id, horoscope_message, parse_mode="Markdown")

# # Start polling
# bot.infinity_polling()

import os
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
VERCEL_URL = os.getenv('VERCEL_URL')  # e.g., "https://your-vercel-deployment-url.vercel.app"

# Validate BOT_TOKEN and VERCEL_URL
if not BOT_TOKEN or not VERCEL_URL:
    raise ValueError("BOT_TOKEN and VERCEL_URL must be set in the environment variables!")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Function to get daily horoscope
def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign."""
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)
    return response.json()

# Handlers for the bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Enter /horoscope to start")

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    # Create an inline keyboard for zodiac signs
    keyboard = InlineKeyboardMarkup()
    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    for sign in zodiac_signs:
        keyboard.add(InlineKeyboardButton(sign, callback_data=f"sign_{sign}"))
    
    text = "Choose your zodiac sign:"
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("sign_"))
def day_handler(call):
    sign = call.data.split("_")[1]
    # Create an inline keyboard for days
    keyboard = InlineKeyboardMarkup()
    days = ["TODAY", "TOMORROW", "YESTERDAY"]
    for day in days:
        keyboard.add(InlineKeyboardButton(day, callback_data=f"day_{sign}_{day}"))
    
    text = f"You selected *{sign}*.\nNow choose a day:"
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
def fetch_horoscope(call):
    _, sign, day = call.data.split("_")
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = (
        f'*Horoscope:* {data["horoscope_data"]}\n'
        f'*Sign:* {sign}\n'
        f'*Day:* {data["date"]}'
    )
    bot.send_message(call.message.chat.id, "Here's your horoscope!")
    bot.send_message(call.message.chat.id, horoscope_message, parse_mode="Markdown")

# Flask webhook route
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    """Handle webhook updates."""
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def index():
    return "Bot is running!", 200

# Set the webhook
@app.before_first_request
def set_webhook():
    webhook_url = f"{VERCEL_URL}/{BOT_TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

# Run the app (Flask)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

