import pytest
from widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("Visa Gold 5999414228426353", "Visa Gold **** ****6353"),
        ("Mastercard Platinum 1234 5678 9876 5432", "Mastercard Platinum **** ****5432"),
        ("Мастеркард 1111222233334444", "Мастеркард **** ****4444"),
        ("Счет 1234567890123456", "Счет **3456"),
        ("Счет 9876543210", "Счет **!"),
        ("Счет 123", "Счет **!"),
        ("Нет данных", "Нет данных"),
        ("", ""),
    ]
)
def test_mask_account_card(input_str, expected_output):
    assert mask_account_card(input_str) == expected_output


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
        ("2022-12-31T23:59:59", "31.12.2022"),
        ("2024-07-15", "15.07.2024"),
    ]
)
def test_get_date_valid(input_str, expected_output):
    assert get_date(input_str) == expected_output


@pytest.mark.parametrize(
    "input_str, expected_exception",
    [
        ("2024-13-01T00:00:00", ValueError),
        ("2024-02-30T00:00:00", ValueError),
        ("Некорректная строка", ValueError),
        ("", ValueError),
    ]
)
def test_get_date_errors(input_str, expected_exception):
    with pytest.raises(expected_exception):
        get_date(input_str)
