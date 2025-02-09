import requests
import json

CURRENCY_NAMES = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
    'usd': 'USD',
    'eur': 'EUR',
    'rub': 'RUB'
}

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()

        if base not in CURRENCY_NAMES or quote not in CURRENCY_NAMES:
            raise APIException(f'Валюта {base} или {quote} не поддерживается.')

        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        base_ticker = CURRENCY_NAMES[base]
        quote_ticker = CURRENCY_NAMES[quote]

        r = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base_ticker}')
        resp = json.loads(r.content)

        if 'rates' not in resp:
            raise APIException('Ошибка при получении данных от API.')

        rate = resp['rates'].get(quote_ticker)
        if rate is None:
            raise APIException(f'Курс для валюты {quote_ticker} не найден.')

        total = rate * amount
        return total