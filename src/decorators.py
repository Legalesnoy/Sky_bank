import json
from functools import wraps
from typing import Callable
import pandas as pd


# from src.reports import df_to_list


def to_json(func: Callable) -> Callable:
    """Декоратор для преобразования результата функции в JSON."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        result = func(*args, **kwargs)
        if isinstance(result, pd.DataFrame):
            result = df_to_list(result)
        result_dict = {func.__name__: result}
        return json.dumps(result_dict, ensure_ascii=False)

    return wrapper


def to_json_file(func: Callable) -> Callable:
    """Декоратор для преобразования результата функции в JSON file."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        result = func(*args, **kwargs)
        if isinstance(result, pd.DataFrame):
            result = df_to_list(result)
        result_dict = {func.__name__: result}

        with open('output.json', 'w') as file:
            json.dump(result_dict, file, ensure_ascii=False)

        return result

    return wrapper


def apply_decorator(funcs, decorator):
    """Декоратор оптом оборачивает список функций в декоратор"""
    return (decorator(func) for func in funcs)


def df_to_list(transactions: pd.DataFrame):
    data_lst = list()
    columns, rows = transactions.shape
    for v in range(columns):
        data_lst.append({k: str(transactions.loc[v, k]) for k in transactions.keys()})
    return data_lst
