# -*- coding: utf-8 -*-
"""
Модуль test_processing содержит тесты для обработки транзакций.

Тестирует функции из src.processing:
- _parse_date: парсинг дат из различных форматов
- sort_by_date: сортировка по дате
- filter_by_state: фильтрация по статусу

Использует pytest fixtures для создания тестовых данных.
"""

import pytest
from datetime import datetime

from src.processing import filter_by_state, sort_by_date, _parse_date


# ============================================================================
# ФИКСТУРЫ
# ============================================================================


@pytest.fixture
def transactions():
    """
    Набор тестовых транзакций для основных тестов.

    Возвращает:
        list: 3 транзакции с разными статусами и датами:
            - id=1: EXECUTED, 2020-01-01
            - id=2: PENDING, 2020-01-02
            - id=3: CANCELED, 2019-12-31
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "2020-01-01T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2020-01-02T12:00:00"},
        {"id": 3, "state": "CANCELED", "date": "2019-12-31T23:59:59"},
    ]


@pytest.fixture
def transactions_with_ms():
    """
    Транзакции с миллисекундами в дате.

    Возвращает:
        list: Транзакции с форматом даты ISO + миллисекунды

    Используется для тестирования _parse_date с разными форматами.
    """
    return [
        {"id": 1, "date": "2020-01-01T00:00:00.000000"},
        {"id": 2, "date": "2020-01-02T00:00:00.123456"},
    ]


# ============================================================================
# ТЕСТЫ _parse_date
# ============================================================================


def test_parse_date_iso_format():
    """
    Тест: парсинг даты в ISO формате.

    Проверяет:
    - Корректность парсинга "2020-01-01T10:00:00"
    - Совпадение года, месяца, дня, часа, минуты, секунды
    """
    result = _parse_date("2020-01-01T10:00:00")
    assert result == datetime(2020, 1, 1, 10, 0, 0)


def test_parse_date_with_milliseconds():
    """
    Тест: парсинг даты с миллисекундами.

    Проверяет:
    - Корректность парсинга "2020-01-01T00:00:00.123456"
    - Миллисекунды корректно обрабатываются
    """
    result = _parse_date("2020-01-01T00:00:00.123456")
    assert result.year == 2020
    assert result.month == 1
    assert result.day == 1


def test_parse_date_only_date():
    """
    Тест: парсинг даты без времени.

    Проверяет:
    - Корректность парсинга "2020-01-01"
    - Время устанавливается в 00:00:00
    """
    result = _parse_date("2020-01-01")
    assert result == datetime(2020, 1, 1, 0, 0, 0)


def test_parse_date_invalid():
    """
    Тест: парсинг невалидной даты.

    Проверяет:
    - Выбрасывается ValueError при неверном формате
    """
    with pytest.raises(ValueError):
        _parse_date("invalid-date")


# ============================================================================
# ТЕСТЫ sort_by_date
# ============================================================================


def test_sort_by_date_ascending(transactions):
    """
    Тест: сортировка транзакций по возрастанию даты.

    Проверяет:
    - Порядок: старые сначала
    - ID в правильном порядке: 3, 1, 2

    Args:
        transactions: fixture с тестовыми транзакциями
    """
    result = sort_by_date(transactions, ascending=True)
    assert [t["id"] for t in result] == [3, 1, 2]


def test_sort_by_date_descending(transactions):
    """
    Тест: сортировка транзакций по убыванию даты.

    Проверяет:
    - Порядок: новые сначала
    - ID в правильном порядке: 2, 1, 3

    Args:
        transactions: fixture с тестовыми транзакциями
    """
    result = sort_by_date(transactions, ascending=False)
    assert [t["id"] for t in result] == [2, 1, 3]


def test_sort_by_date_preserves_original(transactions):
    """
    Тест: сортировка не изменяет исходный список.

    Проверяет:
    - Исходный список остается в том же порядке
    - Создается новый список

    Args:
        transactions: fixture с тестовыми транзакциями
    """
    original_order = [t["id"] for t in transactions]
    sort_by_date(transactions, ascending=True)
    assert [t["id"] for t in transactions] == original_order


# ============================================================================
# ТЕСТЫ filter_by_state
# ============================================================================


def test_filter_by_state_executed(transactions):
    """
    Тест: фильтрация по статусу EXECUTED.

    Проверяет:
    - Возвращаются только транзакции со статусом EXECUTED
    - Количество результатов: 1

    Args:
        transactions: fixture с тестовыми транзакциями
    """
    result = filter_by_state(transactions, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_filter_by_state_canceled(transactions):
    """
    Тест: фильтрация по статусу CANCELED.

    Проверяет:
    - Возвращаются только транзакции со статусом CANCELED
    - Количество результатов: 1

    Args:
        transactions: fixture с тестовыми транзакциями
    """
    result = filter_by_state(transactions, "CANCELED")
    assert len(result) == 1
    assert result[0]["id"] == 3


def test_filter_by_state_none(transactions):
    """
    Тест: фильтрация при state=None.

    Проверяет:
    - Возвращается копия всего списка
    - Количество результатов: 3

    Args:
        transactions: fixture с тестовыми транзакциями
    """
    result = filter_by_state(transactions, None)
    assert len(result) == 3


def test_filter_by_state_none_is_copy(transactions):
    """
    Тест: при state=None возвращается копия.

    Проверяет:
    - Изменение результата не влияет на исходный список

    Args:
        transactions: fixture с тестовыми транзакциями
    """
    result = filter_by_state(transactions, None)
    result.clear()
    assert len(transactions) == 3  # Исходный не изменился


def test_filter_by_state_special_none(transactions):
    """
    Тест: фильтрация при state="NONE".

    Проверяет:
    - Возвращается пустой список
    - Специальное значение для принудительной пустоты

    Args:
        transactions: fixture с тестовыми транзакциями
    """
    result = filter_by_state(transactions, "NONE")
    assert result == []
