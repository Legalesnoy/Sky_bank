import datetime
from typing import Dict, List, Optional

import pandas as pd

from src.decorators import apply_decorator, to_json
from src.utils import str_to_date

"""
The module of basic functions for generating JSON responses

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
    exp_dict: dict = {}

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
    cash: dict = {}
    exp = expenses(transactions)

    for k, v in exp.items():
        for e in v:
            cash[k] = cash.get(k, 0.0)
            cash[k] = round(cash[k], 2) + abs(round(e / 100, 2))
            cash[k] = round(cash[k], 2)
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
    search_data = search_data.lower()

    for transaction in transactions:
        t_str = str(transaction).lower()
        if search_data in t_str:
            result.append(transaction)

    return result


def search_tr_in_data(transactions: List[Dict],
                      date_max: Optional[datetime.datetime | str],
                      date_min: Optional[datetime.datetime | str] = None) -> List[Dict]:
    """функция поиска данных о банковских операций на диапазон дат"""
    result = []

    if (date_max is None) or (date_max == ''):
        date_max = datetime.datetime.now()

    if isinstance(date_max, str):
        date_max = str_to_date(date_max)

    if (date_min is None) or (date_min == ''):
        # расчитываем последние три месяца от переданной даты
        delta = 3  # месяца
        d2_mnth = (date_max.month - delta - 1) % 12 + 1
        d2_year = date_max.year + (date_max.month - delta - 1) // 12
        date_min = datetime.datetime(day=date_max.day, month=d2_mnth, year=d2_year)

    if isinstance(date_min, str):
        date_min = str_to_date(date_min)

    date_min_ = min(date_max, date_min)
    date_max_ = max(date_max, date_min)

    for trans in transactions:
        dt = str_to_data(trans['Дата операции'])
        if date_min_ <= dt <= date_max_:
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
    greeting, top5, cashback, total_expenses, expenses = apply_decorator([greeting, top5, cashback,
                                                                          total_expenses, expenses], to_json)
    print(greeting(10))
    tr = get_transactions("..\\data\\operations.xlsx")
    print(top5(tr))
    l_ = search_transactions(tr, '*5091')
    input(f'найдено {len(l_)} записей')
    for t in l_:
        print(t, '\n')

    # # dd = search_tr_in_data(tr, str_to_data('31.12.2021 16:42:04'))
    # # for d in dd:
    # #     print(d)
    # print(total_expenses(search_tr_in_data(tr, str_to_data('31.12.2021 16:42:04'))))
    # print(cashback(search_tr_in_data(tr, str_to_data('31.12.2021 16:42:04'))))
    # print(top5(search_tr_in_data(tr, str_to_data('31.12.2021 16:42:04'))))
    # # with open("..\\data\\operations.xlsx", "rb") as file1:
    # #     df1 = pd.read_excel(file1,header=0, nrows=0)
    # #     df2 = pd.read_excel(file1, skipfooter=2)
    # # print(extension := file1.name.split(".")[-1])
    # # print(df1.to_dict())
    # # print(df2.shape)
    # #
    #
    #     n_rows = pd.read_excel(file1,usecols='A')
    # print(n_rows.shape[0])
