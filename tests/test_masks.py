import sys
import os

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))

if src_path not in sys.path:
    sys.path.insert(0, src_path)

import masks

# Далее тесты
import pytest
from typing import Any


@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("7000792289606361", "700079** ****6361"),
        ("1234567890", "1234567890"),
        ("12345678901234", "123456** ****1234"),
        ("12345", "12345"),
        (None, ""),
        (1234567890, ""),
    ],
)
def test_get_mask_card_number(input_value: Any, expected: str) -> None:
    assert masks.get_mask_card_number(input_value) == expected


@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("1234567890", "**7890"),
        ("123", "**123"),
        ("", "**"),
        (None, ""),
        (12345, ""),
    ],
)
def test_get_mask_account(input_value: Any, expected: str) -> None:
    assert masks.get_mask_account(input_value) == expected


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
