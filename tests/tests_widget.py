
import pytest
from widget import mask_account_card(), get_date()

@pytest.fixture
def mask_account_test_cases():
    return [
        ("Visa Gold 5999414228426353", "Visa Gold **** ****6353"),
        ("Mastercard Platinum 1234 5678 9876 5432", "Mastercard Platinum **** ****5432"),
        ("Мастеркард 1111222233334444", "Мастеркард **** ****4444"),
        ("Счет 1234567890123456", "Счет **3456"),
        ("Счет 9876543210", "Счет **!"),
        ("Счет 123", "Счет **!"),
        ("Нет данных", "Нет данных"),
        ("", "")
    ]

# Тесты для mask_account_card c фикстурой

def test_mask_account_card_using_fixture(mask_account_test_cases):
    for input_str, expected_output in mask_account_test_cases:
        result = mask_account_card(input_str)
        assert result == expected_output


# Фикстура для тестов get_date

@pytest.fixture
def get_date_valid_cases():
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
        ("2022-12-31T23:59:59", "31.12.2022"),
        ("2024-07-15", "15.07.2024"),
    ]

# Тесты для get_date с валидными данными

def test_get_date_with_valid_cases(get_date_valid_cases):
    for input_str, expected_output in get_date_valid_cases:
        assert get_date(input_str) == expected_output

# Фикстура для тестов get_date — ошибки

@pytest.fixture
def get_date_error_cases():
    return [
        ("2024-13-01T00:00:00", ValueError),
        ("2024-02-30T00:00:00", ValueError),
        ("Некорректная строка", ValueError),
        ("", ValueError),
    ]


# Тесты для get_date — ошибки с фикстурой

def test_get_date_errors(get_date_error_cases):
    for input_str, error_type in get_date_error_cases:
        with pytest.raises(error_type):
            get_date(input_str)

