import telebot
import requests
from telebot import types

TOKEN = "8096000440:AAFyTBVnETPxVEplM3VUQv9slpyBK-fZLMI"

bot = telebot.TeleBot(TOKEN)

def get_rate(currency):
    try:
        url = f"https://open.er-api.com/v6/latest/{currency}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if "rates" not in data:
            return None

        return data["rates"]["RUB"]

    except requests.exceptions.RequestException:
        return "NETWORK_ERROR"

    except Exception:
        return "UNKNOWN_ERROR"


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("USD", "EUR", "CNY")
    keyboard.add("KZT", "UAH", "GBP")
    bot.send_message(
        message.chat.id,
        "Выберите валюту, и я покажу актуальный курс к рублю:",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: message.text in ["USD", "EUR", "CNY", "KZT", "UAH", "GBP"])
def currency_handler(message):
    currency = message.text
    rate = get_rate(currency)

    if rate == "NETWORK_ERROR":
        bot.send_message(message.chat.id, " Ошибка сети. Попробуйте позже.")

    elif rate == "UNKNOWN_ERROR":
        bot.send_message(message.chat.id, " Произошла непредвиденная ошибка.")

    elif rate is None:
        bot.send_message(message.chat.id, " Не удалось получить курс валюты.")

    else:
        bot.send_message(
            message.chat.id,
            f" Курс {currency} к RUB:\n1 {currency} = {rate:.2f} ₽"
        )

@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    bot.send_message(
        message.chat.id,
        " Я вас не понял.\nПожалуйста, выберите валюту с кнопок ниже."
    )


# Запуск бота
bot.polling(none_stop=True)



