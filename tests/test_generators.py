# -*- coding: utf-8 -*-
"""
Модуль test_generators содержит тесты для генераторов транзакций.

Тестирует функции из src.generators:
- filter_by_currency: фильтрация транзакций по валюте
- transaction_descriptions: извлечение описаний транзакций
- card_number_generator: генерация номеров карт с форматированием

Генераторы тестируются:
- С помощью list() для получения всех значений
- С проверкой ленивых вычислений
- С проверкой граничных случаев
"""

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


def test_filter_by_currency():
    """
    Тест: фильтрация транзакций по валюте.

    Проверяет:
    - Возвращаются только транзакции с указанной валютой
    - Количество результатов: 2 для USD
    - Первая транзакция имеет код USD

    Результат: 2 транзакции с USD
    """
    transactions = [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "RUB"}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
    ]

    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert result[0]["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_empty():
    """
    Тест: фильтрация пустого списка.

    Проверяет:
    - Для пустого списка возвращается пустой результат

    Результат: []
    """
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_filter_by_currency_no_match():
    """
    Тест: фильтрация по несуществующей валюте.

    Проверяет:
    - Если нет совпадений, возвращается пустой список

    Результат: []
    """
    transactions = [
        {"operationAmount": {"currency": {"code": "EUR"}}},
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_transaction_descriptions():
    """
    Тест: извлечение описаний из транзакций.

    Проверяет:
    - Количество описаний равно количеству транзакций
    - Порядок описаний сохраняется
    - Текст описаний совпадает

    Результат: ["Payment", "Transfer", "Deposit"]
    """
    transactions = [
        {"description": "Payment"},
        {"description": "Transfer"},
        {"description": "Deposit"},
    ]

    result = list(transaction_descriptions(transactions))
    assert result == ["Payment", "Transfer", "Deposit"]


def test_transaction_descriptions_missing():
    """
    Тест: обработка отсутствующего поля description.

    Проверяет:
    - Для транзакции без description возвращается пустая строка
    - Порядок сохраняется

    Результат: ["Payment", "", "Transfer"]
    """
    transactions = [
        {"description": "Payment"},
        {},  # Нет description
        {"description": "Transfer"},
    ]

    result = list(transaction_descriptions(transactions))
    assert result == ["Payment", "", "Transfer"]


def test_card_number_generator():
    """
    Тест: генерация номеров карт с ведущими нулями.

    Проверяет:
    - Количество сгенерированных номеров: 3
    - Формат: XXXX XXXX XXXX XXXX
    - Ведущие нули добавляются корректно

    Результат: ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    """
    gen = card_number_generator(1, 3)
    result = list(gen)

    assert len(result) == 3
    assert result[0] == "0000 0000 0000 0001"
    assert result[1] == "0000 0000 0000 0002"
    assert result[2] == "0000 0000 0000 0003"


def test_card_number_generator_format():
    """
    Тест: формат номеров карт.

    Проверяет:
    - Формат разделения пробелами: XXXX XXXX XXXX XXXX
    - Каждая часть содержит 4 символа
    - Всего 4 части

    Результат: ["1234 5678 9012 3456"]
    """
    gen = card_number_generator(1234567890123456, 1234567890123456)
    result = list(gen)

    assert len(result) == 1
    # Проверяем формат XXXX XXXX XXXX XXXX
    parts = result[0].split()
    assert len(parts) == 4
    assert all(len(p) == 4 for p in parts)


def test_card_number_generator_single():
    """
    Тест: генерация одного номера с ведущими нулями.

    Проверяет:
    - Один номер генерируется корректно
    - Ведущие нули добавляются

    Результат: ["0000 0000 0000 9999"]
    """
    gen = card_number_generator(9999, 9999)
    result = list(gen)

    assert result[0] == "0000 0000 0000 9999"
