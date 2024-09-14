import os
import pandas as pd
import pytest
from src.views import get_transactions


@pytest.fixture
def transactions():
    if "tests" in os.getcwd():
        file_name = "..\\data\\operations.xlsx"
    else:
        file_name = "data\\operations.xlsx"
    return get_transactions(file_name)


@pytest.fixture
def df_transactions():
    if "tests" in os.getcwd():
        file_name = "..\\data\\operations.xlsx"
    else:
        file_name = "data\\operations.xlsx"
    tr = get_transactions(file_name)
    return pd.DataFrame(tr)
