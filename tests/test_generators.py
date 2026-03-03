from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)

transactions = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2020-01-01T00:00:00",
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Test transaction USD",
    },
    {
        "id": 2,
        "state": "EXECUTED",
        "date": "2020-01-02T00:00:00",
        "operationAmount": {
            "amount": "200.00",
            "currency": {"name": "EUR", "code": "EUR"},
        },
        "description": "Test transaction EUR",
    },
]


def test_filter_by_currency_found():
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_not_found():
    result = list(filter_by_currency(transactions, "RUB"))
    assert result == []


def test_filter_by_currency_empty():
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_transaction_descriptions():
    descs = list(transaction_descriptions(transactions))
    assert descs == ["Test transaction USD", "Test transaction EUR"]


def test_transaction_descriptions_empty():
    assert list(transaction_descriptions([])) == []


def test_card_number_generator_range():
    gen = card_number_generator(1, 3)
    nums = list(gen)
    expected = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    assert nums == expected


def test_card_number_generator_formatting():
    gen = card_number_generator(9999999999999998, 9999999999999999)
    nums = list(gen)
    assert nums[0].startswith("9999 9999 9999 9998")
    assert nums[1].startswith("9999 9999 9999 9999")


def test_card_number_generator_end():
    gen = card_number_generator(9999999999999999, 9999999999999999)
    nums = list(gen)
    assert nums == ["9999 9999 9999 9999"]
