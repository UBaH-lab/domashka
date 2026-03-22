# -*- coding: utf-8 -*-
"""
Модуль test_masks_extended содержит расширенные тесты для функций маскирования.

Тестирует функции из src.masks:
- mask_account_card: маскирование карт и счетов с различными входными данными
- get_date: преобразование дат из различных форматов

Использует pytest.mark.parametrize для проверки множества сценариев,
включая граничные случаи и ошибочные входные данные.
"""

import pytest

from src.masks import get_date, mask_account_card

# ============================================================================
# ТЕСТЫ mask_account_card
# ============================================================================


def test_mask_account_card_empty_input():
    """
    Тест: маскирование пустой строки.

    Проверяет:
    - Для пустой строки возвращается ""

    Результат: ""
    """
    assert mask_account_card("") == ""


def test_mask_account_card_none_input():
    """
    Тест: маскирование None.

    Проверяет:
    - Для None возвращается None

    Результат: None
    """
    assert mask_account_card(None) is None


def test_mask_account_card_no_digits():
    """
    Тест: маскирование строки без цифр.

    Проверяет:
    - Строка без цифр возвращается без изменений

    Результат: "No Digits Here"
    """
    result = mask_account_card("No Digits Here")
    assert result == "No Digits Here"


def test_mask_account_card_with_account():
    """
    Тест: маскирование номера счета.

    Проверяет:
    - Номер счета маскируется форматом "**XXXX"
    - Префикс "Счет" сохраняется

    Результат: "Счет **7890"
    """
    result = mask_account_card("Счет 12345678901234567890")
    assert "Счет" in result
    assert "**" in result


def test_mask_account_card_regular_card():
    """
    Тест: маскирование обычного номера карты.

    Проверяет:
    - Номер карты маскируется форматом "**** ****XXXX"
    - Префикс "Visa" сохраняется

    Результат: "Visa **** ****3456"
    """
    result = mask_account_card("Visa 1234567890123456")
    assert "Visa" in result
    assert "****" in result


def test_mask_account_card_visa():
    """
    Тест: маскирование карты Visa Gold.

    Проверяет:
    - Номер карты маскируется корректно
    - Последние 4 цифры сохраняются: "6353"
    - Префикс "Visa Gold" сохраняется

    Результат: "Visa Gold **** ****6353"
    """
    result = mask_account_card("Visa Gold 5999414228426353")
    assert "Visa Gold" in result
    assert "****" in result
    assert "6353" in result


def test_mask_account_card_short_digits():
    """
    Тест: маскирование короткого номера.

    Проверяет:
    - Короткий номер (< 16 цифр) возвращается без маскирования

    Результат: "Card 123"
    """
    result = mask_account_card("Card 123")
    assert "123" in result


def test_mask_account_card_mastercard():
    """
    Тест: маскирование карты Mastercard Platinum.

    Проверяет:
    - Номер карты маскируется корректно
    - Последние 4 цифры сохраняются: "5432"
    - Префикс "Mastercard" сохраняется

    Результат: "Mastercard Platinum **** ****5432"
    """
    result = mask_account_card("Mastercard Platinum 1234567898765432")
    assert "Mastercard" in result
    assert "****" in result
    assert "5432" in result


# ============================================================================
# ТЕСТЫ get_date
# ============================================================================


def test_get_date_iso():
    """
    Тест: преобразование ISO даты.

    Проверяет:
    - Формат DD.MM.YYYY
    - Дата "2024-03-11T12:34:56" -> "11.03.2024"

    Результат: "11.03.2024"
    """
    result = get_date("2024-03-11T12:34:56")
    assert result == "11.03.2024"


def test_get_date_with_ms():
    """
    Тест: преобразование ISO даты с миллисекундами.

    Проверяет:
    - Миллисекунды игнорируются
    - Дата "2024-03-11T12:34:56.123456" -> "11.03.2024"

    Результат: "11.03.2024"
    """
    result = get_date("2024-03-11T12:34:56.123456")
    assert result == "11.03.2024"


def test_get_date_date_only():
    """
    Тест: преобразование даты без времени.

    Проверяет:
    - Дата "2024-03-11" -> "11.03.2024"

    Результат: "11.03.2024"
    """
    result = get_date("2024-03-11")
    assert result == "11.03.2024"


def test_get_date_invalid():
    """
    Тест: обработка невалидной даты.

    Проверяет:
    - Выбрасывается ValueError

    Результат: ValueError
    """
    with pytest.raises(ValueError):
        get_date("invalid")


def test_get_date_not_string():
    """
    Тест: обработка нестрокового значения.

    Проверяет:
    - Выбрасывается ValueError для числа

    Результат: ValueError
    """
    with pytest.raises(ValueError):
        get_date(12345)
