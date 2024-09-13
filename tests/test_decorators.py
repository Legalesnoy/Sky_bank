from src.decorators import to_json, to_json_file, apply_decorator, df_to_list


def test_to_json():
    @to_json
    @to_json_file('test')
    def _aaa():
        return 'oooo'

    assert _aaa() == '{"_aaa": "oooo"}'

    with open('test', 'r') as file:
        oooo = file.read()
        assert oooo == '{"_aaa": "oooo"}'


def test_apply_decorator():
    def _aaa():
        return 'oooo'

    _aaa, = apply_decorator([_aaa, ], to_json)
    assert _aaa() == '{"_aaa": "oooo"}'


def test_df_to_list(df_transactions, transactions):
    assert df_to_list(df_transactions) == transactions
