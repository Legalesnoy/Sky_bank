from src.reports import df_to_list, spending_by_category, spending_by_weekday, spending_by_workday


def test_df_to_list(df_transactions, transactions):
    assert df_to_list(df_transactions) == transactions


def test_spending_by_category(df_transactions, transactions):
    df1 = spending_by_category(transactions, "Супермаркеты", "01.02.2019")
    assert len(df1) == 115
    df2 = spending_by_category(df_transactions, "Супермаркеты", "01.02.2019")
    assert df1.compare(df2).empty
    df3 = spending_by_category(df_transactions, "Красота", "01.02.2019")
    assert len(df3) == 1


def test_spending_by_weekday(df_transactions):
    df = spending_by_weekday(df_transactions, "01.01.2019")
    assert df.iloc[0]["Средние траты"] == 1568.15


def test_spending_by_workday(df_transactions):
    df = spending_by_workday(df_transactions, "01.01.2019")
    assert df.iloc[0]["Средние траты"] == 1748.55
