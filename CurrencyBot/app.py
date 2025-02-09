import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter, CURRENCY_NAMES

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    instructions = (
        "Отправьте сообщение в формате: <имя валюты> <в какую валюту перевести> <количество>\n"
        "Пример: доллар рубль 100\n"
        "Доступные валюты: доллар (USD), евро (EUR), рубль (RUB)"
    )
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['values'])
def send_values(message):
    currencies = "\n".join([f"{name} ({code})" for name, code in CURRENCY_NAMES.items()])
    bot.reply_to(message, f"Доступные валюты:\n{currencies}")

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров. Нужно ввести три значения.')

        base, quote, amount = values
        total = CurrencyConverter.get_price(base, quote, amount)
        text = f'Цена {amount} {base} в {quote} : {total:.2f}'
        bot.send_message(message.chat.id, text)

    except APIException as e:
        bot.reply_to(message, f"Ошибка:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка:\n{e}")

bot.polling()