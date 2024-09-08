import datetime

from src.utils import get_currency_rate2, get_spx_index
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

    valute_lst = ('USD', 'EUR', 'CNY', 'BYN', 'JPY')
    print(f"\nКурс валют на {datetime.datetime.now().date().strftime("%d.%m.%Y")}:")
    course = get_currency_rate2(datetime.datetime.now().date(), valute_lst)
    for rate in course:
        print(f"{rate['currency_code']} = {rate['rate']}")
    print("\nКурс S&P500:")
    spx_lst = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    for spx in spx_lst:
        print(spx, get_spx_index(spx)['price'])

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