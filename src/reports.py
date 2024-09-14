import datetime
import json
from typing import Dict, List, Optional

import pandas as pd

from src.decorators import apply_decorator, to_json, to_json_file
from src.utils import str_to_date
from src.views import search_tr_in_data, search_transactions


def df_to_list(transactions: pd.DataFrame):
    return list(transactions.to_dict("index").values())


def spending_by_category(
    transactions: pd.DataFrame | List[Dict],
    name_category: str,
    date1: Optional[str | datetime.datetime] = None,
    date2: Optional[str | datetime.datetime] = None,
):
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    if (date1 is None) or (date1 == ""):
        date1 = datetime.datetime.now()

    if isinstance(date1, str):
        date1 = str_to_date(date1)

    if (date2 is None) or (date2 == ""):
        # расчитываем последние три месяца от переданной даты
        delta = 3  # месяца
        d2_mnth = (date1.month - delta - 1) % 12 + 1
        d2_year = date1.year + (date1.month - delta - 1) // 12
        date2 = datetime.datetime(day=date1.day, month=d2_mnth, year=d2_year)

    if isinstance(date2, str):
        date2 = str_to_date(date2)

    if isinstance(transactions, pd.DataFrame):
        data_lst = df_to_list(transactions)
    else:
        data_lst = transactions

    result = search_transactions(data_lst, f"'Категория': '{name_category}'")
    result = search_tr_in_data(result, date1, date2)

    return pd.DataFrame(result)


def spending_by_weekday(
    transactions: pd.DataFrame | List[Dict],
    date1: Optional[str | datetime.datetime] = None,
    date2: Optional[str | datetime.datetime] = None,
) -> pd.DataFrame:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца
    от переданной даты либо диапазона дат"""
    weekday = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    expenses_lst: dict = {k: [] for k in weekday}
    average_expenses = {k: 0.0 for k in weekday}

    if isinstance(transactions, pd.DataFrame):
        data_lst = df_to_list(transactions)
    else:
        data_lst = transactions
    if (date1 is None) or (date1 == ""):
        date1 = datetime.datetime.now()

    if isinstance(date1, str):
        date1 = str_to_date(date1)

    if (date2 is None) or (date2 == ""):
        # расчитываем последние три месяца от переданной даты
        delta = 3  # месяца
        d2_mnth = (date1.month - delta - 1) % 12 + 1
        d2_year = date1.year + (date1.month - delta - 1) // 12
        date2 = datetime.datetime(day=date1.day, month=d2_mnth, year=d2_year)

    if isinstance(date2, str):
        date2 = str_to_date(date2)

    data = search_tr_in_data(data_lst, date1, date2)

    for oprtn in data:
        dt_op = str_to_date(oprtn["Дата операции"])  # date_operation
        d = weekday[dt_op.weekday()]
        expense = float(oprtn["Сумма платежа"])
        if expense < 0:  # наверное, пополнения не учитываем - только расходы
            expenses_lst[d].append(-expense)

    for day in expenses_lst.keys():
        s = sum(expenses_lst[day])
        l_ = len(expenses_lst[day]) | 1
        average_expenses[day] = round(s / l_, 2)

    return (
        pd.DataFrame.from_dict(average_expenses, orient="index", columns=["Средние траты"])
        .reset_index()
        .rename(columns={"index": "День недели"})
    )


def spending_by_workday(
    transactions: pd.DataFrame | List[Dict],
    date1: Optional[str | datetime.datetime] = None,
    date2: Optional[str | datetime.datetime] = None,
) -> pd.DataFrame:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца
    от переданной даты либо диапазона дат."""

    expenses = {"рабочие дни": 0.0, "выходные": 0.0}

    if isinstance(transactions, pd.DataFrame):
        transactions = df_to_list(transactions)

    s_w = spending_by_weekday(transactions, date1, date2)
    if isinstance(s_w, str):
        s_w = json.loads(s_w)
        first_key = list(s_w.keys())[0]
        s_w = pd.DataFrame(s_w[first_key])
    average_expenses = dict(zip(s_w["День недели"], s_w["Средние траты"])).values()

    for d, trans in enumerate(average_expenses):
        if d < 5:
            expenses["рабочие дни"] += float(trans)
        else:
            expenses["выходные"] += float(trans)

    expenses["рабочие дни"] = round(expenses["рабочие дни"] / 5, 2)
    expenses["выходные"] = round(expenses["выходные"] / 2, 2)

    return (
        pd.DataFrame.from_dict(expenses, orient="index", columns=["Средние траты"])
        .reset_index()
        .rename(columns={"index": "Дни недели"})
    )


if __name__ == "__main__":
    from src.decorators import apply_decorator, to_json, to_json_file
    from src.views import get_transactions, greeting

    spending_by_category, spending_by_weekday, spending_by_workday = apply_decorator(
        [spending_by_category, spending_by_weekday, spending_by_workday], to_json_file()
    )
    # spending_by_category, spending_by_weekday, spending_by_workday = (
    #     apply_decorator([spending_by_category, spending_by_weekday, spending_by_workday], to_json))

    print(greeting(10))
    tr = get_transactions("..\\data\\operations.xlsx")
    tr_df = pd.DataFrame(tr)
    # df_lst = list(tr_df.to_dict('index').values())
    # print(tr_df)
    # print(tr[0:5])
    # print()
    # print(df_lst[0:5])
    tr_cat = spending_by_category(tr_df, "Каршеринг", "01.01.2024", "01.01.2017")
    print(tr_cat)
    print(spending_by_weekday(tr_cat, "01.01.2024", "01.01.2017"))
    print(spending_by_workday(tr_cat, "01.01.2024", "01.01.2017"))
