from src.reports import df_to_list, spending_by_category


def test_df_to_list(df_transactions, transactions):
    assert df_to_list(df_transactions) == transactions


def test_spending_by_category(transactions):

    df = spending_by_category(transactions,'','01.01.2024', '01.01.2024')
    assert len(df.head()) == 0

def test_spending_by_weekday():
    ...


def test_spending_by_workday():
    ...



