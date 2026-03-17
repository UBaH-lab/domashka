"""Модуль для работы с банковскими транзакциями."""

import json
import logging
from typing import List, Dict, Any, Optional

from src.masks import get_mask_card_number
from src.transactions_reader import read_transactions_csv, read_transactions_excel

# Настройка логирования с записью в файл
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="logs/app.log",
    encoding="utf-8",
)

logger = logging.getLogger(__name__)

STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Загружено {len(data)} транзакций из JSON: {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        print(f"Программа: Файл {file_path} не найден.")
        return []
    except json.JSONDecodeError:
        logger.error("Ошибка декодирования JSON")
        print("Программа: Ошибка при чтении JSON-файла.")
        return []


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из CSV-файла."""
    try:
        data = read_transactions_csv(file_path)
        logger.info(f"Загружено {len(data)} транзакций из CSV: {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        print(f"Программа: Файл {file_path} не найден.")
        return []
    except ValueError as e:
        logger.error(f"Ошибка чтения CSV: {e}")
        print(f"Программа: {e}")
        return []


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из XLSX-файла."""
    try:
        data = read_transactions_excel(file_path)
        logger.info(f"Загружено {len(data)} транзакций из XLSX: {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        print(f"Программа: Файл {file_path} не найден.")
        return []
    except ValueError as e:
        logger.error(f"Ошибка чтения XLSX: {e}")
        print(f"Программа: {e}")
        return []


def get_valid_status() -> Optional[str]:
    """Запрашивает у пользователя статус с валидацией."""
    while True:
        print('Программа: Введите статус, по которому необходимо выполнить фильтрацию.')
        print(f'Доступные для фильтровки статусы: {", ".join(STATUSES)}')
        user_input = input("Пользователь: ").strip().upper()
        if user_input in STATUSES:
            print(f'Программа: Операции отфильтрованы по статусу "{user_input}"')
            return user_input
        else:
            print(f'Программа: Статус операции "{user_input}" недоступен.\n')


def filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    result = []
    for item in data:
        item_status = item.get("state", item.get("status", ""))
        if item_status and item_status.upper() == status:
            result.append(item)
    return result


def sort_by_date(data: List[Dict[str, Any]], ascending: bool = False) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""
    def parse_date(date_str: str) -> tuple:
        try:
            parts = date_str.split(".")
            if len(parts) == 3:
                return (int(parts[2]), int(parts[1]), int(parts[0]))
        except (ValueError, AttributeError):
            pass
        return (0, 0, 0)
    return sorted(data, key=lambda x: parse_date(x.get("date", "")), reverse=not ascending)


def filter_by_currency(data: List[Dict[str, Any]], currency: str = "RUB") -> List[Dict[str, Any]]:
    """Фильтрует транзакции по валюте."""
    result = []
    for item in data:
        item_currency = item.get("operationAmount", {}).get("currency", {}).get("code", "")
        if not item_currency:
            item_currency = item.get("currency", "")
        if item_currency == currency:
            result.append(item)
    return result


def mask_number(number: str) -> str:
    """Маскирует номер карты или счета."""
    if not number:
        return ""
    digits = "".join(c for c in number if c.isdigit())
    if len(digits) == 16:
        return get_mask_card_number(digits)
    elif len(digits) > 16:
        return f"**{digits[-4:]}"
    return number


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода."""
    lines = []
    date = transaction.get("date", "")
    description = transaction.get("description", "")
    lines.append(f"{date} {description}")

    from_acc = transaction.get("from", "")
    to_acc = transaction.get("to", "")

    if from_acc and to_acc:
        from_parts = from_acc.split()
        to_parts = to_acc.split()
        from_type = " ".join(from_parts[:-1]) if len(from_parts) > 1 else ""
        from_number = from_parts[-1] if from_parts else ""
        masked_from = f"{from_type} {mask_number(from_number)}" if from_type else mask_number(from_number)
        to_type = " ".join(to_parts[:-1]) if len(to_parts) > 1 else ""
        to_number = to_parts[-1] if to_parts else ""
        masked_to = f"{to_type} {mask_number(to_number)}" if to_type else mask_number(to_number)
        lines.append(f"{masked_from} -> {masked_to}")
    elif to_acc:
        to_parts = to_acc.split()
        to_type = " ".join(to_parts[:-1]) if len(to_parts) > 1 else ""
        to_number = to_parts[-1] if to_parts else ""
        masked_to = f"{to_type} {mask_number(to_number)}" if to_type else mask_number(to_number)
        lines.append(masked_to)

    amount = transaction.get("operationAmount", {}).get("amount", transaction.get("amount", 0))
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code", transaction.get("currency", ""))
    if currency_code == "RUB":
        currency_code = "руб."
    lines.append(f"Сумма: {amount} {currency_code}")
    return "\n".join(lines)


def ask_yes_no(question: str) -> bool:
    """Задает вопрос с ответом да/нет."""
    print(f"Программа: {question}")
    answer = input("Пользователь: ").strip().lower()
    return answer in ("да", "yes", "y", "д")


def main() -> None:
    """Главная функция программы."""
    logger.info("Запуск программы")

    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()
    data: List[Dict[str, Any]] = []

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        file_path = input("Программа: Введите путь к файлу: ").strip()
        data = load_transactions_from_json(file_path)
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        file_path = input("Программа: Введите путь к файлу: ").strip()
        data = load_transactions_from_csv(file_path)
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        file_path = input("Программа: Введите путь к файлу: ").strip()
        data = load_transactions_from_excel(file_path)
    else:
        print("Программа: Неверный выбор.")
        return

    if not data:
        return

    status = get_valid_status()
    if not status:
        return

    filtered_data = filter_by_status(data, status)

    if ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        print("Программа: Введите 'по возрастанию' или 'по убыванию':")
        order = input("Пользователь: ").strip().lower()
        ascending = "возрастани" in order
        filtered_data = sort_by_date(filtered_data, ascending)

    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        filtered_data = filter_by_currency(filtered_data, "RUB")

    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
        print("Программа: Введите слово для поиска:")
        search_word = input("Пользователь: ").strip()
        if search_word:
            from bank_utils import process_bank_search
            filtered_data = process_bank_search(filtered_data, search_word)

    print("Программа: Распечатываю итоговый список транзакций...\n")

    if not filtered_data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"Всего банковских операций в выборке: {len(filtered_data)}\n")
    for transaction in filtered_data:
        print(format_transaction(transaction))
        print()

    logger.info(f"Выведено {len(filtered_data)} транзакций")


if __name__ == "__main__":
    main()