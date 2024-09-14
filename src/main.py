import datetime

from src.reports import (spending_by_category, spending_by_weekday,
                         spending_by_workday)
from src.utils import get_currency_rate2, get_spx_index
from src.views import (cashback, get_transactions, greeting, search_tr_in_data,
                       top5, total_expenses)

if __name__ == "__main__":
    tr = get_transactions("..\\data\\operations.xlsx")

    print(greeting())
    print('Введите на дату(либо диапазон дат) для вывода статистики:')
    date1 = input('введите превую дату:')
    date2 = input('введите вторую дату либо пропустите:')
    if date2 != '':
        print(f"На период {date1} - {date2} общая сумма расходов:")
    else:
        print(f"На период {date1} общая сумма расходов за 3 мес.:")
    tr_date = search_tr_in_data(tr, date1, date2)
    te = total_expenses(tr_date)
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
    category = input('Напишите по какой категории вывести транзакции:')
    print('На какую дату(либо диапазон дат):')
    date1 = input('введите превую дату:')
    date2 = input('введите вторую дату либо пропустите:')
    tr_cat = spending_by_category(tr, category, date1, date2)
    print(f'транзакции по категории:\n{tr_cat}\n')
    print(f'статистика по дням недели:\n{spending_by_weekday(tr_cat, date1, date2)}\n')
    print(f'Итого в рабочие/выходные дни:\n{spending_by_workday(tr_cat, date1, date2)}\n')
