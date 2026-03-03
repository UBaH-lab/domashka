import pytest
from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator
)

# Пример списка транзакций для тестирования
transactions = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2020-01-01T00:00:00",
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Test transaction USD"
    },
    {
        "id": 2,
        "state": "EXECUTED",
        "date": "2020-01-02T00:00:00",
        "operationAmount": {
            "amount": "200.00",
            "currency": {
                "name": "EUR",
                "code": "EUR"
            }
        },
        "description": "Test transaction EUR"
    }
]


def test_filter_by_currency_found():
    # Проверяем, что функция фильтрует транзакции по валюте правильно
    result = list(filter_by_currency(transactions, "USD"))
    # В результирующем списке должна быть ровно одна транзакция
    assert len(result) == 1
    # Убедимся, что ID совпадает
    assert result[0]["id"] == 1
    # Валюта транзакции должна быть 'USD'
    assert result[0]["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_not_found():
    # Проверка, что при отсутствии транзакций в указанной валюте,
    # возвращается пустой список
    result = list(filter_by_currency(transactions, "RUB"))
    assert result == []


def test_filter_by_currency_empty():
    # Проверка, что при передаче пустого списка транзакций
    # функция не вызывает ошибок и возвращает пустой список
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_transaction_descriptions():
    # Проверка, что генератор возвращает правильные описания транзакций
    gen = transaction_descriptions(transactions)
    # Собираем все описания в список
    descs = list(gen)
    # Проверяем, что описания совпадают с ожидаемыми
    assert descs == ["Test transaction USD", "Test transaction EUR"]


def test_transaction_descriptions_empty():
    # Проверка, что при пустом списке транзакций генератор возвращает пустой список
    gen = transaction_descriptions([])
    assert list(gen) == []


def test_card_number_generator_range():
    # Тест генератора номеров карт с диапазоном от 1 до 3
    gen = card_number_generator(1, 3)
    nums = list(gen)
    # Ожидаемые номера с ведущими нулями и разбиты на группы по 4
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]
    # Проверяем, что генерируемые номера совпадают с ожидаемыми
    assert nums == expected


def test_card_number_generator_formatting():
    # Проверка форматирования номеров карт в диапазоне, близком к максимуму
    gen = card_number_generator(9999999999999998, 9999999999999999)
    nums = list(gen)
    # Первое число должно начинаться с ожидаемой последовательности
    assert nums[0].startswith("9999 9999 9999 9998")
    # Второе должно быть максимально возможным номером
    assert nums[1].startswith("9999 9999 9999 9999")


def test_card_number_generator_end():
    # Проверка работы генератора при диапазоне из одного числа
    gen = card_number_generator(9999999999999999, 9999999999999999)
    nums = list(gen)
    # В результате должна быть ровно одна карта
    assert nums == ["9999 9999 9999 9999"]