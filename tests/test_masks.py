import sys
import os
import pytest

# Добавляем путь к папке src, где находится masks.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Импортируем модуль напрямую
from src import masks

@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("7000792289606361", "700079** ****6361"),
        ("1234567890", "1234567890"),
        ("12345678901234", "123456** ****1234"),
        ("12345", "12345"),
        (None, ""),
        (1234567890, ""),
    ]
)
def test_get_mask_card_number(input_value, expected):
    assert masks.get_mask_card_number(input_value) == expected

@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("1234567890", "**7890"),
        ("123", "**123"),
        ("", "**"),
        (None, ""),
        (12345, ""),
    ]
)
def test_get_mask_account(input_value, expected):
    assert masks.get_mask_account(input_value) == expected

if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])