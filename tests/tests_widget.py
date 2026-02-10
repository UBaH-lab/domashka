
import pytest
from src.masks import get_mask_card_number
from widget.py import mask_account_card

@pytest.mark.parametrize("input_str, expected_output", [
    # Карты
    ("Visa Gold 5999414228426353", "Visa Gold 599941******2635"),
    ("MasterCard Platinum 1234 5678 9012 3456", "MasterCard Platinum 1234 5678 9012 3456"),  # предполагается, что get_mask_card_number маскирует
    ("Maestro 4539 1488 0343 6467", "Maestro 4539 1488 0343 6467"),
    # Счета
    ("Счёт 1234567890", "Счет **7890"),
    ("Счёт 987654321", "Счет **4321"),
])
def test_mask_account_card(input_str, expected_output):
    result = mask_account_card(input_str)
    assert result == expected_output

# Тесты на некорректные данные
@pytest.mark.parametrize("input_str", [
    "",                     # пустая строка
    "SomeRandomText",       # без слова "Счёт" и номера
    "Счёт",                # без номера
    "Visa",                 # только название карты
    "Счёт 123",             # короткий номер счета
    None,                   # None (если функция должна её обрабатывать)
])
def test_mask_account_card_invalid(input_str):
    # Допустим, функция должна возвращать строку или бросать исключение
    if input_str is None:
        with pytest.raises(Exception):
            mask_account_card(input_str)
    else:
        result = mask_account_card(input_str)
        assert isinstance(result, str)

        from src.masks import get_date

        def test_get_date_correct():
            assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
            assert get_date("2020-01-01T00:00:00") == "01.01.2020"
            assert get_date("1999-12-31T23:59:59") == "31.12.1999"

        def test_get_date_with_various_formats():
            # Проверка, что функция парсит только первые 10 символов
            assert get_date("2024-07-15ExtraText") == "15.07.2024"
            # В случае некорректной строки
            with pytest.raises(ValueError):
                get_date("InvalidDateString")
            # В случае строки короче 10 символов
            with pytest.raises(ValueError):
                get_date("2024-03")