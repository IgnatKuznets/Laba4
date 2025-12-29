import telebot
import requests
import pandas as pd
from telebot import types

# Токен Telegram-бота
TOKEN = "8096000440:AAFyTBVnETPxVEplM3VUQv9slpyBK-fZLMI"

bot = telebot.TeleBot(TOKEN)

# Список поддерживаемых валют
CURRENCIES = ["USD", "EUR", "CNY", "KZT", "UAH", "GBP"]

# Функция получения курса выбранной валюты
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


# Функция получения всех курсов валют и формирования DataFrame
def get_all_rates_dataframe():
    data = []

    for currency in CURRENCIES:
        rate = get_rate(currency)
        if isinstance(rate, (int, float)):
            data.append({
                "Валюта": currency,
                "Курс к RUB": round(rate, 2)
            })

    df = pd.DataFrame(data)
    return df


# Команда /start
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


# Обработка выбора валюты
@bot.message_handler(func=lambda message: message.text in CURRENCIES)
def currency_handler(message):
    currency = message.text
    rate = get_rate(currency)

    if rate == "NETWORK_ERROR":
        bot.send_message(message.chat.id, "Ошибка сети. Попробуйте позже.")

    elif rate == "UNKNOWN_ERROR":
        bot.send_message(message.chat.id, "Произошла непредвиденная ошибка.")

    elif rate is None:
        bot.send_message(message.chat.id, "Не удалось получить курс валюты.")

    else:
        bot.send_message(
            message.chat.id,
            f"Курс {currency} к RUB:\n1 {currency} = {rate:.2f} ₽"
        )


# Команда /analysis для анализа данных с использованием pandas
@bot.message_handler(commands=["analysis"])
def analysis(message):
    df = get_all_rates_dataframe()

    if df.empty:
        bot.send_message(message.chat.id, "Не удалось получить данные для анализа.")
        return

    max_currency = df.loc[df["Курс к RUB"].idxmax()]
    min_currency = df.loc[df["Курс к RUB"].idxmin()]

    text = "Анализ курсов валют:\n\n"

    for _, row in df.iterrows():
        text += f"{row['Валюта']}: {row['Курс к RUB']} ₽\n"

    text += f"\nСамая дорогая валюта: {max_currency['Валюта']}"
    text += f"\nСамая дешёвая валюта: {min_currency['Валюта']}"

    bot.send_message(message.chat.id, text)


# Обработка произвольного текста пользователя
@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    bot.send_message(
        message.chat.id,
        "Команда не распознана. Используйте кнопки или команды /start и /analysis."
    )


# Запуск бота
bot.polling(none_stop=True)




