# -*- coding: utf-8 -*-
"""
Модуль test_processing_extended содержит расширенные тесты для обработки транзакций.

Тестирует функции из src.processing:
- _parse_date: парсинг дат из различных форматов
- sort_by_date: сортировка транзакций по дате
- filter_by_state: фильтрация транзакций по статусу

Использует pytest.mark.parametrize для проверки множества сценариев.
"""

import pytest
from src.processing import sort_by_date, filter_by_state, _parse_date


# ============================================================================
# ТЕСТЫ _parse_date
# ============================================================================


def test_parse_date_iso():
    """
    Тест: парсинг ISO даты с временем.

    Проверяет:
    - Год: 2024
    - Месяц: 3
    - День: 11

    Результат: datetime(2024, 3, 11, 12, 34, 56)
    """
    result = _parse_date("2024-03-11T12:34:56")
    assert result.year == 2024
    assert result.month == 3
    assert result.day == 11


def test_parse_date_with_ms():
    """
    Тест: парсинг ISO даты с миллисекундами.

    Проверяет:
    - Год: 2024

    Результат: datetime(2024, 3, 11, 12, 34, 56, 123456)
    """
    result = _parse_date("2024-03-11T12:34:56.123456")
    assert result.year == 2024


def test_parse_date_simple():
    """
    Тест: парсинг простой даты без времени.

    Проверяет:
    - Год: 2024
    - Месяц: 3
    - День: 11

    Результат: datetime(2024, 3, 11)
    """
    result = _parse_date("2024-03-11")
    assert result.year == 2024
    assert result.month == 3
    assert result.day == 11


def test_parse_date_invalid():
    """
    Тест: парсинг невалидной даты.

    Проверяет:
    - Выбрасывается ValueError

    Результат: ValueError
    """
    with pytest.raises(ValueError):
        _parse_date("invalid-date")


# ============================================================================
# ТЕСТЫ sort_by_date
# ============================================================================


def test_sort_by_date_ascending():
    """
    Тест: сортировка по возрастанию даты.

    Проверяет:
    - Порядок: старые сначала
    - ID: [2, 3, 1]

    Результат: [{"id": 2}, {"id": 3}, {"id": 1}]
    """
    transactions = [
        {"id": 1, "date": "2024-03-11"},
        {"id": 2, "date": "2024-01-01"},
        {"id": 3, "date": "2024-02-15"},
    ]

    result = sort_by_date(transactions, ascending=True)
    assert result[0]["id"] == 2  # Самая старая
    assert result[2]["id"] == 1  # Самая новая


def test_sort_by_date_descending():
    """
    Тест: сортировка по убыванию даты.

    Проверяет:
    - Порядок: новые сначала
    - ID: [1, 3, 2]

    Результат: [{"id": 1}, {"id": 3}, {"id": 2}]
    """
    transactions = [
        {"id": 1, "date": "2024-03-11"},
        {"id": 2, "date": "2024-01-01"},
        {"id": 3, "date": "2024-02-15"},
    ]

    result = sort_by_date(transactions, ascending=False)
    assert result[0]["id"] == 1  # Самая новая
    assert result[2]["id"] == 2  # Самая старая


def test_sort_by_date_with_time():
    """
    Тест: сортировка с учетом времени.

    Проверяет:
    - Транзакции сортируются по дате и времени
    - ID: [2, 1]

    Результат: [{"id": 2}, {"id": 1}]
    """
    transactions = [
        {"id": 1, "date": "2024-03-11T10:00:00"},
        {"id": 2, "date": "2024-03-11T08:00:00"},
    ]

    result = sort_by_date(transactions, ascending=True)
    assert result[0]["id"] == 2


# ============================================================================
# ТЕСТЫ filter_by_state
# ============================================================================


def test_filter_by_state_executed():
    """
    Тест: фильтрация по статусу EXECUTED.

    Проверяет:
    - Возвращаются только транзакции со статусом EXECUTED
    - Количество: 2

    Результат: [{"id": 1}, {"id": 3}]
    """
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]

    result = filter_by_state(transactions, "EXECUTED")
    assert len(result) == 2
    assert all(t["state"] == "EXECUTED" for t in result)


def test_filter_by_state_none():
    """
    Тест: фильтрация при state=None.

    Проверяет:
    - Возвращается копия всего списка
    - Количество: 2

    Результат: [{"id": 1}, {"id": 2}]
    """
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]

    result = filter_by_state(transactions, None)
    assert len(result) == 2


def test_filter_by_state_none_string():
    """
    Тест: фильтрация при state="NONE".

    Проверяет:
    - Возвращается пустой список

    Результат: []
    """
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]

    result = filter_by_state(transactions, "NONE")
    assert result == []


def test_filter_by_state_canceled():
    """
    Тест: фильтрация по статусу CANCELED.

    Проверяет:
    - Возвращаются только транзакции со статусом CANCELED
    - Количество: 1
    - ID: 2

    Результат: [{"id": 2}]
    """
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]

    result = filter_by_state(transactions, "CANCELED")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_state_no_match():
    """
    Тест: фильтрация по несуществующему статусу.

    Проверяет:
    - Возвращается пустой список

    Результат: []
    """
    transactions = [
        {"id": 1, "state": "EXECUTED"},
    ]

    result = filter_by_state(transactions, "PENDING")
    assert result == []


def test_filter_by_state_missing_field():
    """
    Тест: фильтрация при отсутствии поля state.

    Проверяет:
    - Транзакции без поля state не возвращаются
    - Количество: 1
    - ID: 1

    Результат: [{"id": 1}]
    """
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2},  # Нет поля state
    ]

    result = filter_by_state(transactions, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 1
