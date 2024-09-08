import os

import pytest

from src.views import get_transactions


@pytest.fixture
def transactions():
    if 'tests' in os.getcwd():
        file_name = "..\\data\\operations.xlsx"
    else:
        file_name = "data\\operations.xlsx"
    return get_transactions(file_name)
