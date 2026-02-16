import masks  # импортируем сюда, чтобы потом передавать в фикстуру
import sys
import os
import pytest

# Добавляем путь к папке src, где находится модуль masks.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


@pytest.fixture
def masks_module():
    # возвращаем модуль для использования в тестах
    return masks


@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("7000792289606361", "700079** ****6361"),  # стандартный 16
        ("1234567890", "1234567890"),               # 10 символов (короткий)
        ("12345678901234", "123456** ****1234"),   # 14 символов
        ("12345", "12345"),                         # очень короткий
        (None, ""),                                 # не строка None
        (1234567890, ""),                           # не строка int
    ]
)
def test_get_mask_card_number(masks_module, input_value, expected):
    assert masks_module.get_mask_card_number(input_value) == expected


@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("1234567890", "**7890"),  # стандартный
        ("123", "**123"),          # короче 4 символов
        ("", "**"),                # пустая строка
        (None, ""),                # не строка None
        (12345, ""),               # не строка int
    ]
)
def test_get_mask_account(masks_module, input_value, expected):
    assert masks_module.get_mask_account(input_value) == expected


if __name__ == "__main__":
    # Запуск тестов программно
    pytest.main([os.path.abspath(__file__)])
