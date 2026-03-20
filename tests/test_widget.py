# -*- coding: utf-8 -*-
"""
Модуль test_widget содержит тесты для виджетов маскирования.

Тестирует функции из src.widget:
- mask_account_card: маскирование карт и счетов
- get_date: преобразование даты
- get_mask_card_number: упрощенное маскирование карты

Использует parametrize для проверки множества вариантов.
"""

import pytest

from src.widget import get_date, mask_account_card, get_mask_card_number


# ============================================================================
# ФИКСТУРЫ
# ============================================================================


@pytest.fixture
def input_str_mask(request):
    """
    Возвращает строку-исходник для маскировки карт/счётов.

    Значение приходит через request.param благодаря indirect-переменной в тестах.

    Returns:
        str: Строка с названием и номером карты/счёта

    Examples:
        - "Visa Gold 5999414228426353"
        - "Счет 12345678901234567890"
    """
    return request.param


@pytest.fixture
def input_str_date_valid(request):
    """
    Возвращает валидную ISO-строку даты/времени для теста get_date.

    Значение приходит через request.param благодаря indirect-переменной в тестах.

    Returns:
        str: Дата в ISO формате

    Examples:
        - "2024-03-11T12:34:56.123456"
        - "2024-03-11"
    """
    return request.param


@pytest.fixture
def input_str_date_invalid(request):
    """
    Возвращает невалидную строку для теста ошибок get_date.

    Returns:
        str: Невалидная строка даты
    """
    return request.param


# ============================================================================
# ТЕСТЫ mask_account_card
# ============================================================================


@pytest.mark.parametrize(
    "input_str_mask, expected_output",
    [
        ("Visa Gold 5999414228426353", "Visa Gold **** ****6353"),
        (
            "Mastercard Platinum 1234 5678 9876 5432",
            "Mastercard Platinum **** ****5432",
        ),
        ("Мастеркард 1111222233334444", "Мастеркард **** ****4444"),
        ("Счет 1234567890123456", "Счет **3456"),
        ("Счет 123", "Счет **123"),
        ("Счет 9876543210", "Счет **3210"),
        ("Нет данных", "Нет данных"),
        ("", ""),
        (None, None),
    ],
    indirect=["input_str_mask"],
)
def test_mask_account_card(input_str_mask, expected_output):
    """
    Тест: маскирование карт и счетов.

    Проверяет:
    - Формат маски для карт: "префикс **** ****XXXX"
    - Формат маски для счетов: "префикс **XXXX"
    - Обработка пустых строк и None
    - Обработка коротких номеров

    Args:
        input_str_mask: входная строка (через fixture)
        expected_output: ожидаемый результат
    """
    result = mask_account_card(input_str_mask)
    assert result == expected_output


# ============================================================================
# ТЕСТЫ get_date
# ============================================================================


@pytest.mark.parametrize(
    "input_str_date_valid, expected_output",
    [
        ("2024-03-11T12:34:56.123456", "11.03.2024"),
        ("2024-03-11T12:34:56", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("2024-12-01", "01.12.2024"),
    ],
    indirect=["input_str_date_valid"],
)
def test_get_date_valid(input_str_date_valid, expected_output):
    """
    Тест: преобразование валидных дат.

    Проверяет:
    - Формат DD.MM.YYYY
    - Обработка разных ISO форматов
    - Корректность дня и месяца

    Args:
        input_str_date_valid: входная дата (через fixture)
        expected_output: ожидаемый результат
    """
    result = get_date(input_str_date_valid)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_str_date_invalid",
    [
        "invalid",
        "2024/03/11",
        "11.03.2024",
        "",
        None,
    ],
    indirect=["input_str_date_invalid"],
)
def test_get_date_invalid(input_str_date_invalid):
    """
    Тест: обработка невалидных дат.

    Проверяет:
    - Выбрасывается ValueError или TypeError
    - Некорректные форматы отвергаются

    Args:
        input_str_date_invalid: невалидная строка (через fixture)
    """
    with pytest.raises((ValueError, TypeError)):
        get_date(input_str_date_invalid)


# ============================================================================
# ТЕСТЫ get_mask_card_number
# ============================================================================


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "123456** ****3456"),
        ("0000000000000000", "000000** ****0000"),
        ("1111222233334444", "111122** ****4444"),
    ],
)
def test_get_mask_card_number(card_number, expected):
    """
    Тест: упрощенное маскирование номера карты.

    Проверяет:
    - Формат: "XXXXXX** ****XXXX"
    - Первые 6 цифр сохраняются
    - Последние 4 цифры сохраняются

    Args:
        card_number: номер карты (16 цифр)
        expected: ожидаемый результат
    """
    result = get_mask_card_number(card_number)
    assert result == expected


def test_get_mask_card_number_short():
    """
    Тест: маскирование короткого номера.

    Проверяет:
    - Короткий номер возвращается без изменений
    """
    result = get_mask_card_number("12345")
    assert result == "12345"


def test_get_mask_card_number_none():
    """
    Тест: маскирование None.

    Проверяет:
    - None возвращается без изменений
    """
    result = get_mask_card_number(None)
    assert result is None
