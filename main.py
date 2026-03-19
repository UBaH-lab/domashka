"""Модуль для работы с банковскими транзакциями.

Этот модуль предоставляет функционал для загрузки, фильтрации, сортировки
и форматирования банковских транзакций из различных форматов файлов
(JSON, CSV, XLSX).

Основные возможности:
    - Загрузка транзакций из файлов разных форматов
    - Фильтрация по статусу, валюте, ключевым словам
    - Сортировка по дате
    - Маскировка номеров карт и счетов
    - Подсчет операций по категориям
    - Форматированный вывод результатов

Пример использования:
    >>> python main.py
    >>> # Следуйте интерактивным подсказкам программы

"""

import json
import logging
from typing import List, Dict, Any, Optional

from src.masks import get_mask_card_number
from src.transactions_reader import read_transactions_csv, read_transactions_excel
from bank_utils import process_bank_search, process_bank_operations

# Настройка логирования с записью в файл
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="logs/app.log",
    encoding="utf-8",
)

logger = logging.getLogger(__name__)

# Допустимые статусы транзакций для фильтрации
STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
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
    """Загружает транзакции из XLSX-файла (Excel)."""
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
    """Запрашивает у пользователя статус транзакции с валидацией."""
    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
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


def sort_by_date(
    data: List[Dict[str, Any]], ascending: bool = False
) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""

    def parse_date(date_str: str) -> tuple:
        try:
            parts = date_str.split(".")
            if len(parts) == 3:
                return (int(parts[2]), int(parts[1]), int(parts[0]))
        except (ValueError, AttributeError):
            pass
        return (0, 0, 0)

    return sorted(
        data, key=lambda x: parse_date(x.get("date", "")), reverse=not ascending
    )


def filter_by_currency(
    data: List[Dict[str, Any]], currency: str = "RUB"
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по валюте."""
    result = []
    for item in data:
        item_currency = (
            item.get("operationAmount", {}).get("currency", {}).get("code", "")
        )
        if not item_currency:
            item_currency = item.get("currency", "")
        if item_currency == currency:
            result.append(item)
    return result


def mask_number(number: str) -> str:
    """Маскирует номер карты или счёта для безопасного отображения."""
    if not number:
        return ""

    digits = "".join(c for c in number if c.isdigit())

    if len(digits) == 16:
        return get_mask_card_number(digits)
    elif len(digits) > 16:
        return f"**{digits[-4:]}"
    else:
        return number


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль."""
    date = transaction.get("date", "")
    description = transaction.get("description", "")

    from_info = transaction.get("from", "")
    to_info = transaction.get("to", "")

    from_masked = mask_number(from_info) if from_info else ""
    to_masked = mask_number(to_info) if to_info else ""

    amount = ""
    currency = ""
    op_amount = transaction.get("operationAmount")
    if op_amount:
        amount = op_amount.get("amount", "")
        curr_info = op_amount.get("currency", {})
        currency = curr_info.get("name", curr_info.get("code", ""))

    lines = []
    header = f"{date} {description}" if date and description else date or description
    if header:
        lines.append(header)

    if from_masked and to_masked:
        lines.append(f"{from_masked} -> {to_masked}")
    elif to_masked:
        lines.append(f"-> {to_masked}")

    if amount and currency:
        lines.append(f"Сумма: {amount} {currency}.")

    return "\n".join(lines)


# =============================================================================
# Вспомогательные функции для main (снижение сложности)
# =============================================================================


def _select_file_format() -> Optional[str]:
    """Выводит меню выбора формата файла и возвращает выбор пользователя.

    Returns:
        Optional[str]: 'json', 'csv', 'xlsx' или None при ошибке.
    """
    print(
        "Программа: Привет! Добро пожаловать в программу работы\n"
        "с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )

    user_choice = input("Пользователь: ").strip()

    if user_choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        return "json"
    elif user_choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        return "csv"
    elif user_choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        return "xlsx"
    else:
        print("Программа: Некорректный выбор. Завершение работы.")
        return None


def _load_transactions_by_format(file_format: str) -> List[Dict[str, Any]]:
    """Запрашивает имя файла и загружает транзакции в зависимости от формата.

    Args:
        file_format (str): Формат файла ('json', 'csv', 'xlsx').

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список при ошибке.
    """
    print("Программа: Введите название файла:")
    filename = input("Пользователь: ").strip()

    if file_format == "json":
        return load_transactions_from_json(filename)
    elif file_format == "csv":
        return load_transactions_from_csv(filename)
    elif file_format == "xlsx":
        return load_transactions_from_excel(filename)
    else:
        print("Программа: Неизвестный формат файла.")
        return []


def _filter_by_status_interactive(
    transactions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Интерактивная фильтрация по статусу.

    Args:
        transactions: Список транзакций.

    Returns:
        Отфильтрованный список транзакций.
    """
    status = get_valid_status()
    return filter_by_status(transactions, status)


def _sort_by_date_interactive(
    transactions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Интерактивная сортировка по дате.

    Args:
        transactions: Список транзакций.

    Returns:
        Отсортированный список транзакций.
    """
    print("Программа: Введите порядок сортировки (по возрастанию / по убыванию):")
    order = input("Пользователь: ").strip().lower()

    if order in ["по возрастанию", "возрастание", "asc"]:
        print("Программа: Транзакции отсортированы по возрастанию.")
        return sort_by_date(transactions, ascending=True)
    else:
        print("Программа: Транзакции отсортированы по убыванию.")
        return sort_by_date(transactions, ascending=False)


def _filter_by_currency_interactive(
    transactions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Интерактивная фильтрация по валюте.

    Args:
        transactions: Список транзакций.

    Returns:
        Отфильтрованный список транзакций.
    """
    print("Программа: Введите код валюты для фильтрации (например, RUB, USD, EUR):")
    currency = input("Пользователь: ").strip().upper()
    print(f"Программа: Транзакции отфильтрованы по валюте {currency}.")
    return filter_by_currency(transactions, currency)


def _search_by_keywords(transactions: List[Dict[str, Any]]) -> None:
    """Интерактивный поиск по ключевым словам.

    Args:
        transactions: Список транзакций.
    """
    print("Программа: Введите ключевое слово для поиска в описаниях транзакций:")
    keyword = input("Пользователь: ").strip()

    results = process_bank_search(transactions, keyword)
    print(f"Программа: Найдено {len(results)} транзакций по запросу '{keyword}':")

    for t in results[:5]:
        print(format_transaction(t))
        print()


def _show_category_statistics(transactions: List[Dict[str, Any]]) -> None:
    """Выводит статистику по категориям транзакций.

    Args:
        transactions: Список транзакций.
    """
    categories = ["перевод", "оплата", "снятие", "пополнение"]
    stats = process_bank_operations(transactions, categories)

    print("Программа: Статистика по категориям:")
    for category, count in stats.items():
        print(f"  {category}: {count}")


def _display_results(transactions: List[Dict[str, Any]]) -> None:
    """Выводит итоговые транзакции пользователю.

    Args:
        transactions: Список транзакций для вывода.
    """
    if not transactions:
        print("Программа: Нет транзакций для отображения.")
        return

    print(f"Программа: Всего транзакций: {len(transactions)}")
    print("Программа: Вывод первых 5 транзакций:")

    for i, t in enumerate(transactions[:5], 1):
        print(f"\n--- Транзакция {i} ---")
        print(format_transaction(t))


# =============================================================================
# Главная функция
# =============================================================================


def main() -> None:
    """Главный модуль с интерактивным интерфейсом.

    Функция запускает интерактивный CLI-интерфейс для работы
    с банковскими транзакциями. Пользователь пошагово выбирает:
    формат файла, фильтры, сортировку и параметры вывода.

    Основные шаги:
        1. Приветствие и выбор формата файла
        2. Загрузка данных из файла
        3. Фильтрация по статусу
        4. Сортировка по дате (опционально)
        5. Фильтрация по валюте (опционально)
        6. Поиск по ключевым словам (опционально)
        7. Вывод результатов
    """
    # Шаг 1: Выбор формата файла
    file_format = _select_file_format()
    if not file_format:
        return

    # Шаг 2: Загрузка данных
    transactions = _load_transactions_by_format(file_format)
    if not transactions:
        print("Программа: Не удалось загрузить транзакции.")
        return

    # Шаг 3: Фильтрация по статусу
    transactions = _filter_by_status_interactive(transactions)

    # Шаг 4: Сортировка по дате
    print("Программа: Нужна ли сортировка по дате? (да/нет):")
    need_sort = input("Пользователь: ").strip().lower()
    if need_sort in ["да", "yes", "y", "д"]:
        transactions = _sort_by_date_interactive(transactions)

    # Шаг 5: Фильтрация по валюте
    print("Программа: Нужна ли фильтрация по валюте? (да/нет):")
    need_currency = input("Пользователь: ").strip().lower()
    if need_currency in ["да", "yes", "y", "д"]:
        transactions = _filter_by_currency_interactive(transactions)

    # Шаг 6: Поиск по ключевым словам
    print("Программа: Нужен ли поиск по ключевым словам? (да/нет):")
    need_search = input("Пользователь: ").strip().lower()
    if need_search in ["да", "yes", "y", "д"]:
        _search_by_keywords(transactions)

    # Шаг 7: Статистика по категориям
    print("Программа: Вывести статистику по категориям? (да/нет):")
    need_stats = input("Пользователь: ").strip().lower()
    if need_stats in ["да", "yes", "y", "д"]:
        _show_category_statistics(transactions)

    # Шаг 8: Вывод результатов
    _display_results(transactions)

    print("\nПрограмма: Завершение работы. До свидания!")


if __name__ == "__main__":
    main()
