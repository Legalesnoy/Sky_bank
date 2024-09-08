import datetime
import re
from typing import List, Dict

import pandas as pd

"""
The module of basic functions for generating JSON responses
Модуль основных функций для генерации JSON-ответов
"""

"""
Реализован набор функций и главную функцию, принимающую на вход строку с датой и временем в формате 
YYYY-MM-DD HH:MM:SS  и возвращающую JSON-ответ со следующими данными:

Приветствие в формате 
"???", где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
1. По каждой карте:
    последние 4 цифры карты;
    общая сумма расходов total_expenses;
    кешбэк (1 рубль на каждые 100 рублей).
2. Топ-5 транзакций по сумме платежа.
"""


def expenses(transactions: List[Dict]) -> Dict:
    """функция возвращающая номера карт со списком расходов """
    exp_dict = {}

    for trans in transactions:
        sum_op = float(trans['Сумма операции'])

        if sum_op < 0:
            exp_dict[trans['Номер карты']] = exp_dict.get(trans['Номер карты'], list())
            exp_dict[trans['Номер карты']].append(sum_op)

    return exp_dict


def total_expenses(transactions: List[Dict]) -> Dict:
    """функция возвращающая общую сумму расходов по каждой карте"""
    total_exp_dict = expenses(transactions)

    for k in total_exp_dict.keys():
        total_exp_dict[k] = abs(sum(total_exp_dict[k]))

    return total_exp_dict


def cashback(transactions: List[Dict]) -> dict:
    """функция возвращающая расчёт суммы кэшбэка с расходов по каждой карте"""
    cash = {}
    exp = expenses(transactions)

    for k, v in exp.items():
        for e in v:
            cash[k] = cash.get(k, 0.0)
            cash[k] = round(cash[k], 2) + abs(round(e / 100, 2))

    return cash


def top5(transactions: List[Dict]) -> list[dict]:
    """функция возвращающая топ 5 транзакций по сумме платежа"""

    transactions.sort(key=lambda x: float(x['Сумма операции']))
    return transactions[0:5]


def greeting(hour: int | None = None) -> str:
    """функция приветсвия входящие параметры - значение времени"""
    greeting_str = "Добрый день!"
    if hour is not None:
        h = hour
    else:
        h = datetime.datetime.now().hour

    if 0 <= h < 6:
        greeting_str = "Доброй ночи!"
    elif 6 <= h < 12:
        greeting_str = "Доброе утро!"
    elif 18 <= h < 24:
        greeting_str = "Добрый вечер!"

    return greeting_str


def get_transactions(file_name: str) -> List[Dict]:
    "получает данные из excel файла"
    data_lst = list()

    df = pd.read_excel(file_name)
    columns, rows = df.shape
    for v in range(columns):
        data_lst.append({k: str(df.loc[v, k]) for k in df.keys()})
    return data_lst


def search_transactions(transactions: List[Dict], search_data: str) -> List[Dict]:
    """функция поиска данных о банковских операций"""
    result = []

    for transaction in transactions:

        t_str = str(transaction).lower()
        pattern = re.compile(search_data.lower())

        if re.search(pattern, t_str, flags=0) is not None:
            result.append(transaction)

    return result


def search_tr_in_data(transactions: List[Dict], date_max: datetime.datetime) -> List[Dict]:
    """функция поиска данных о банковских операций на диапазон дат"""
    result = []
    date_min = date_max.replace(day=1, hour=0, minute=0, second=0)

    for trans in transactions:
        dt = str_to_data(trans['Дата операции'])
        if date_min <= dt <= date_max:
            result.append(trans)

    return result


def str_to_data(date_string: str) -> datetime.datetime:
    """преобразует дату формата 31.12.2021 в формат date"""

    if len(date_string.split()) == 1:
        date_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y")
    else:
        date_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y %H:%M:%S")

    return date_obj


if __name__ == "__main__":
    print(greeting())
    # print(str_to_data('31.12.2021'))
    tr = get_transactions("..\\data\\operations.xlsx")
    print(search_transactions(tr, '31.12.2021 16:42:04'))
    # dd = search_tr_in_data(tr, str_to_data('31.12.2021 16:42:04'))
    # for d in dd:
    #     print(d)
    print(total_expenses(search_tr_in_data(tr, str_to_data('31.12.2021 16:42:04'))))
    print(cashback(search_tr_in_data(tr, str_to_data('31.12.2021 16:42:04'))))
    print(top5(search_tr_in_data(tr, str_to_data('31.12.2021 16:42:04'))))
    # with open("..\\data\\operations.xlsx", "rb") as file1:
    #     df1 = pd.read_excel(file1,header=0, nrows=0)
    #     df2 = pd.read_excel(file1, skipfooter=2)
    # print(extension := file1.name.split(".")[-1])
    # print(df1.to_dict())
    # print(df2.shape)
    #
    #
    #     n_rows = pd.read_excel(file1,usecols='A')
    # print(n_rows.shape[0])
