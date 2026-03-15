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
    - Счет: префикс до цифр + "**" + последние 4 цифры.
    - Неверные/пустые данные возвращаются без изменений.
    """
    assert mask_account_card(input_str_mask) == expected_output


@pytest.mark.parametrize(
    "input_str_date_valid, expected_output",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
        ("2022-12-31T23:59:59", "31.12.2022"),
        ("2024-07-15", "15.07.2024"),
    ],
)
def test_get_date_valid(input_str_date_valid, expected_output):
    """
    Тестирует преобразование даты к формату DD.MM.YYYY.

    Поддерживаются варианты с временной частью (ISO-формат) и без неё.
    """
    assert get_date(input_str_date_valid) == expected_output


@pytest.mark.parametrize(
    "input_str_date_err, expected_exception",
    [
        ("2024-13-01T00:00:00", ValueError),
        ("2024-02-30T00:00:00", ValueError),
        ("Некорректная строка", ValueError),
        ("", ValueError),
    ],
)
def test_get_date_errors(input_str_date_err, expected_exception):
    """
    Проверяет, что неверный ввод вызывает ValueError.

    Включены:
    - неправильные месяц/день
    - строка, не являющаяся датой
    - пустая строка
    """
    with pytest.raises(expected_exception):
        get_date(input_str_date_err)
