import datetime

from src.utils import get_currency_rate
from src.views import greeting, total_expenses, get_transactions, search_tr_in_data, str_to_data, top5, cashback
from collections import abc
if __name__ == "__main__":
    tr = get_transactions("..\\data\\operations.xlsx")
    tr_date = search_tr_in_data(tr, str_to_data('05.12.2021'))
    print(greeting())
    print("На 05.12.2021 общая сумма расходов:")
    te=total_expenses(tr_date)
    for k in te:
        print(f"  карта {k} - {te[k]}")
    cash = cashback(tr_date)
    print("Кэшбэк:")
    for k in cash:
        print(f"  карта {k} - {cash[k]}")
    print("Топ-5 транзакций по сумме платежа:")
    top = top5(tr_date)
    for t in top:
        print(f"  {abs(float(t['Сумма операции']))} {t['Валюта операции']} - {t['Описание']} {t['Категория']}")

    valute_lst = ['USD', 'EUR', 'CNY', 'BYN', 'JPY']
    print(f"Курс валют на {datetime.datetime.now().date().strftime("%d.%m.%Y")}:")

    for v in valute_lst:
        course = get_currency_rate(datetime.datetime.now().date(),v)
        print(f"{v} = {course['rate']}")

"""
Задачи по категориям:
   1. Веб-страницы:
        Главная
        События
        
   2. Сервисы:
        Выгодные категории повышенного кешбэка
        Инвесткопилка
        Простой поиск
        Поиск по телефонным номерам
        Поиск переводов физическим лицам
        
   3. Отчеты:
        Траты по категории
        Траты по дням недели
        Траты в рабочий/выходной день
"""