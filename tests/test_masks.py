# -*- coding: utf-8 -*-
"""
Модуль test_masks содержит тесты для функций маскирования.

Тестирует функции из src.masks:
- mask_account_card: маскирование карт и счетов
- get_date: преобразование даты

Использует pytest.mark.parametrize для проверки множества сценариев.
"""

import pytest

from src.masks import get_date, mask_account_card

# Описание тестов:
# - test_mask_account_card проверяет маскирование для карт и счетов.
# - test_get_date_valid проверяет форматирование дат в DD.MM.YYYY.
# - test_get_date_errors убеждается, что неверный ввод вызывает ValueError.


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
    ],
)
def test_mask_account_card(input_str_mask, expected_output):
    """
    Тестирует логику маскировки для двух типов входных данных:
    - Карта: префикс до цифр + "**** ****" + последние 4 цифры.
    - Счёт: префикс до цифр + "**" + последние 4 цифры.

    Args:
        input_str_mask: Входная строка с названием и номером
        expected_output: Ожидаемый результат маскирования

    Examples:
        >>> mask_account_card("Visa Gold 1234567890123456")
        "Visa Gold **** ****3456"
    """
    assert mask_account_card(input_str_mask) == expected_output


@pytest.mark.parametrize(
    "input_date, expected_output",
    [
        ("2024-03-11T12:34:56.123456", "11.03.2024"),
        ("2024-03-11T12:34:56", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("2024-12-01", "01.12.2024"),
    ],
)
def test_get_date_valid(input_date, expected_output):
    """
    Тестирует корректное форматирование дат в формат DD.MM.YYYY.

    Args:
        input_date: Дата в ISO формате
        expected_output: Дата в формате DD.MM.YYYY

    Examples:
        >>> get_date("2024-03-11")
        "11.03.2024"
    """
    assert get_date(input_date) == expected_output


@pytest.mark.parametrize(
    "invalid_input",
    [
        "invalid",
        "2024/03/11",
        "11.03.2024",
        "",
    ],
)
def test_get_date_errors(invalid_input):
    """
    Проверяет, что при невалидном формате даты выбрасывается ValueError.

    Args:
        invalid_input: Невалидная строка даты

    Examples:
        >>> get_date("invalid")
        ValueError: Invalid date format
    """
    with pytest.raises(ValueError):
        get_date(invalid_input)


def test_get_date_type_error():
    """
    Проверяет, что при передаче не строки выбрасывается ValueError.

    Функция ожидает строку, другие типы должны вызывать ошибку.
    """
    with pytest.raises(ValueError):
        get_date(None)
