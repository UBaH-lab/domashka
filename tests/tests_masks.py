import sys
import os

# Добавляем путь к папке src, где находится модуль masks.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import masks  # импортируем весь модуль

def test_get_mask_card_number():
    # Стандартный номер (длина 16)
    assert masks.get_mask_card_number("7000792289606361") == "700079** ****6361"
    # Менее 16 символов, например 10
    assert masks.get_mask_card_number("1234567890") == "1234567890"
    # 14 символов
    assert masks.get_mask_card_number("12345678901234") == "123456** ****1234"
    # Очень короткий номер
    assert masks.get_mask_card_number("12345") == "12345"
    # Не строка
    assert masks.get_mask_card_number(None) == ""
    assert masks.get_mask_card_number(1234567890) == ""

def test_get_mask_account():
    # стандартный номер
    assert masks.get_mask_account("1234567890") == "**7890"
    # короче 4 символов
    assert masks.get_mask_account("123") == "**123"
    assert masks.get_mask_account("") == "**"
    # не строка
    assert masks.get_mask_account(None) == ""
    assert masks.get_mask_account(12345) == ""

if __name__ == "__main__":
    test_get_mask_card_number()
    test_get_mask_account()
    print("Все тесты прошли успешно!")