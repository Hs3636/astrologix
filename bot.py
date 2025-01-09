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
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Validate BOT_TOKEN
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")

# Initialize Flask app
app = Flask(__name__)

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign."""
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)
    return response.json()

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

@app.route('/')
def home():
    return 'Bot is running!'

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)