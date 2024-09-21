import os

from src.views import (
    expenses,
    get_transactions,
    total_expenses,
    cashback,
    top5,
    greeting,
    search_transactions,
    str_to_data,
)


def test_expenses(transactions):
    assert len(expenses(transactions)["*7197"]) == 4811


def test_total_expenses(transactions):
    assert total_expenses(transactions)["*7197"] == 2_389_912.73


def test_cashback(transactions):
    assert cashback(transactions)["*7197"] == 23_899.78


def test_top5(transactions):
    assert len(top5(transactions)) == 5


def test_greeting():
    assert greeting(0) == "Доброй ночи!"


def test_get_transactions():
    if "tests" in os.getcwd():
        file_name = "..\\data\\operations.xlsx"
    else:
        file_name = "data\\operations.xlsx"

    assert len(get_transactions(file_name)) == 6705


def test_search_transactions(transactions):
    search_data = "31.12.2021 16:42:04"
    field = "Дата операции"
    assert search_transactions(transactions, search_data)[0][field] == search_data


def test_str_to_data():
    test_str = "31.12.2021 16:42:04"
    assert str_to_data(test_str).day == 31
    assert str_to_data(test_str).month == 12
    assert str_to_data(test_str).year == 2021
    assert str_to_data(test_str).hour == 16
    assert str_to_data(test_str).minute == 42
