"""
Скрипт для проверки работы логирования.
"""

import json
from pathlib import Path

from masks import get_date, mask_account_card
from utils import read_transactions_json


def main():
    """Проверка логирования в модулях."""
    print("=== Проверка логирования ===")

    # Тест masks
    print("\nТест masks:")
    print(mask_account_card("Visa Gold 5999414228426353"))
    print(mask_account_card("Счет 1234567890123456"))
    print(mask_account_card("Текст без цифр"))
    print(mask_account_card(""))

    try:
        print(get_date("2024-03-11T02:26:18.671407"))
        print(get_date("некорректная дата"))
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    # Тест utils
    print("\nТест utils:")

    # Создадим тестовый файл
    test_file = Path("test_transactions.json")
    test_data = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"},
    ]

    test_file.write_text(json.dumps(test_data), encoding="utf-8")
    print(read_transactions_json(str(test_file)))

    # Тест с несуществующим файлом
    print(read_transactions_json("nonexistent.json"))

    # Удаляем тестовый файл
    test_file.unlink()

    print("\n=== Проверьте папку logs/ ===")
    print("Файлы логов: masks.log и utils.log")


if __name__ == "__main__":
    main()
