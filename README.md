# Horoscope Bot

A simple Telegram bot that provides daily horoscopes for various zodiac signs. This bot uses inline buttons for users to select their zodiac sign and preferred day (TODAY, TOMORROW, or YESTERDAY), and fetches horoscope data from an external API.
**Access Link: ** @astrologix_horoscope_bot

## Features

- **Zodiac Sign Selection:** Users can select their zodiac sign from a list of options using inline buttons.
- **Day Selection:** After selecting the sign, users can choose the day they want to receive a horoscope for (TODAY, TOMORROW, YESTERDAY).
- **Horoscope Fetching:** The bot fetches horoscope data from an external API based on the user's selections.
- **Clean User Interface:** The bot uses inline buttons to make the interaction smooth and efficient.

## Requirements

Before running the bot, ensure you have the following:

- **Python 3** installed on your system.
- A **Telegram Bot Token**, which you can get by chatting with [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
- The **dotenv** library to manage your environment variables.
- The **requests** library for making HTTP requests.

## API

The bot fetches horoscope data from the following API:

- **API URL:** `https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily`
- **Parameters:**
  - `sign`: The user's zodiac sign (e.g., Aries, Taurus).
  - `day`: The date in `YYYY-MM-DD` format or options like `TODAY`, `TOMORROW`, or `YESTERDAY`.
