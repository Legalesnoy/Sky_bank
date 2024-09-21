from unittest.mock import patch

from src.utils import str_to_date, get_currency_rate1, get_currency_rate2, get_spx_index


def test_str_to_date():
    test_str = "1/12/2021"
    assert str_to_date(test_str).day == 1
    assert str_to_date(test_str).month == 12
    assert str_to_date(test_str).year == 2021


@patch("src.utils.requests.get")
def test_get_currency_rate1(mock_get):
    result = {"date": "01.12.2021", "currency_code": "USD", "rate": 20}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"Valute": {"USD": {"Value": 20}}}
    assert get_currency_rate1("1/12/2021", "USD") == result


@patch("src.utils.requests.get")
def test_get_currency_rate2(mock_get):
    result = [{"date": "01.12.2021", "currency_code": "USD", "rate": 2.11}]
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = (
        "<ValCurs>"
        '<Valute ID = "123">'
        "<CharCode>USD</CharCode><VunitRate>2.11</VunitRate>"
        "</Valute>"
        '<Valute ID = "333"><CharCode>qqq</CharCode></Valute></ValCurs>'
    )
    assert get_currency_rate2("1/12/2021", "USD") == result


@patch("src.utils.requests.get")
def test_get_spx_index(mock_get):
    result = {"stock": "AAPL", "price": 220}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"Global Quote": {"05. price": 220}}
    assert get_spx_index("AAPL") == result
