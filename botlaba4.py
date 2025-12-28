import telebot
import requests
from telebot import types

TOKEN = "8096000440:AAFyTBVnETPxVEplM3VUQv9slpyBK-fZLMI"

bot = telebot.TeleBot(TOKEN)

# Получение курса валют
def get_rate(currency):
    url = f"https://open.er-api.com/v6/latest/{currency}"
    response = requests.get(url)
    data = response.json()

    if "rates" not in data:
        return None

    return data["rates"]["RUB"]

# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("USD", "EUR", "CNY")
    bot.send_message(
        message.chat.id,
        "Выберите валюту, и я покажу актуальный курс к рублю:",
        reply_markup=keyboard
    )

# Обработка выбора валюты
@bot.message_handler(func=lambda message: message.text in ["USD", "EUR", "CNY"])
def currency_handler(message):
    currency = message.text
    rate = get_rate(currency)
    bot.send_message(
        message.chat.id,
        f"💱 Курс {currency} к RUB:\n1 {currency} = {rate:.2f} ₽"
    )

# Запуск бота
bot.polling(none_stop=True)

