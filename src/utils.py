import datetime
import json
import os
import re
from typing import Dict, List, Tuple

import requests
import xmltodict
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
"""
Модуль для вывода
- курса валют
- стоимости акций из S&P500.

"""


def str_to_date(date_str: str) -> datetime.datetime:
    """функция преобразует строку в формат datetime"""
    time_str = "00:00:00"

    if len(date_str) > len("01/01/1999 "):
        str_1, str_2 = date_str.split(" ", 1)
        if ":" in str_1:
            time_str, date_str = str_1, str_2
        elif ":" in str_2:
            time_str, date_str = str_2, str_1

    time_format = "%H:%M:%S"
    time_ = datetime.datetime.strptime(time_str, time_format).time()

    try:
        date_lst = list(map(int, re.findall(r"\d+", date_str)))
        d_year = [y for y in date_lst if y > 31][-1]
        date_lst.remove(d_year)
        d_month = [m for m in date_lst if 0 < m <= 12][-1]
        date_lst.remove(d_month)
        d_day = date_lst[0]
        return datetime.datetime(
            year=d_year, month=d_month, day=d_day, hour=time_.hour, minute=time_.minute, second=time_.second
        )
    except ValueError:
        raise ValueError("Неверный формат даты")


def get_currency_rate1(date: str | datetime.date, currency_code: List | str) -> Dict:
    """функция получающая курс валюты, json"""
    if type(date) is str:
        date = str_to_date(date)
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    header = {"apikey": API_KEY}
    params = {"date_req": date.strftime("%d/%m/%Y")}
    response = requests.get(url, headers=header, params=params)

    if response.status_code != 200:
        raise ValueError(f"Failed to get currency rate for date {date}")

    data = response.json()
    currency_data = data["Valute"].get(currency_code)

    if not currency_data:
        raise ValueError(f"No data for currency {currency_code}")

    rates = {"date": date.strftime("%d.%m.%Y"), "currency_code": currency_code, "rate": currency_data["Value"]}

    with open("user_settings.json", "w") as file:
        json.dump(rates, file)

    return rates


def get_currency_rate2(date: str | datetime.date, currency_code: Tuple[str, ...] | str) -> List[Dict]:
    """функция получающая курс валюты, XML"""
    if type(date) is str:
        date = str_to_date(date)
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    params = {"date_req": date.strftime("%d/%m/%Y")}
    header = {"apikey": API_KEY}
    response = requests.get(url, headers=header, params=params, stream=True)
    if response.status_code != 200:
        raise ValueError(f"Failed to get currency rate for date {date}")

    currency_data = xmltodict.parse(response.content)["ValCurs"]["Valute"]
    currency_data = filter(lambda x: x["CharCode"] in currency_code, currency_data)

    rates = []
    for rate in currency_data:
        rates.append(
            {
                "date": date.strftime("%d.%m.%Y"),
                "currency_code": rate.get("CharCode"),
                "rate": round(float(rate.get("VunitRate").replace(",", ".")), 2),
            }
        )

    with open("user_settings.json", "w") as file:
        json.dump(rates, file)

    return rates


def get_spx_index(stock, date: str | datetime.date = datetime.datetime.now().date()) -> Dict:
    """Функция возвращающая курс акций"""
    stock_price = {"stock": stock, "price": "undefined"}
    if type(date) is str:
        date = str_to_date(date)
    API_KEY_STOCK = os.environ.get("API_KEY_STOCK")
    url = "https://www.alphavantage.co/query"
    header = {"apikey": API_KEY_STOCK}
    params = {"function": "GLOBAL_QUOTE", "symbol": stock, "date": date.strftime("%Y-%m-%d")}
    params.update(header)

    resp = requests.get(url, params=params)

    if resp.status_code == 200:
        json_dct = dict(resp.json())
        price = json_dct.get("Global Quote", {}).get("05. price", None)
        stock_price["price"] = price

    return stock_price


if __name__ == "__main__":
    print(get_currency_rate2("1/12/2021", "USD"))
    print(get_spx_index("AAPL"))
    # print(get_currency_rate(datetime.datetime.now().date(),'EUR'))
    # print(get_currency_rate(datetime.datetime.now().date(),'CNY'))
    # print(get_currency_rate(datetime.datetime.now().date(),'BYN'))
    # print(get_currency_rate(datetime.datetime.now().date(),'JPY'))
