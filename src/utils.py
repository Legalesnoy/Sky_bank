import json
import logging
import os
import datetime

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
"""
Курс валют.
Стоимость акций из S&P500.

"""

def get_currency_rate(date, currency_code):
    """функция получающая курс валюты"""
    url = f"https://www.cbr-xml-daily.ru/daily_json.js"
    header = {"apikey": API_KEY}
    response = requests.get(url, headers=header)
    if response.status_code != 200:
        raise ValueError(f"Failed to get currency rate for date {date}")
    data = response.json()
    currency_data = data["Valute"].get(currency_code)
    if not currency_data:
        raise ValueError(f"No data for currency {currency_code}")
    rates = {"date": date, "currency_code": currency_code, "rate": currency_data["Value"]}

    # with open("user_settings.json", "w") as file:
    #     json.dump(rates, file)

    return rates


if __name__ == "__main__":
    print(datetime.datetime.now().date())
    print(get_currency_rate(datetime.datetime.now().date(),'USD'))
    print(get_currency_rate(datetime.datetime.now().date(),'EUR'))
    print(get_currency_rate(datetime.datetime.now().date(),'CNY'))
    print(get_currency_rate(datetime.datetime.now().date(),'BYN'))
    print(get_currency_rate(datetime.datetime.now().date(),'JPY'))


