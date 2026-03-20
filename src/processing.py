# -*- coding: utf-8 -*-
"""
Модуль processing содержит функции для обработки и фильтрации транзакций.

Основные операции:
- Сортировка транзакций по дате
- Фильтрация по статусу (EXECUTED, CANCELED и т.д.)
- Парсинг дат из различных форматов

Эти функции используются для подготовки данных перед отображением.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


def _parse_date(date_str: str) -> datetime:
    """
    Приватная функция для преобразования строки даты в объект datetime.

    Поддерживает несколько форматов:
    - ISO формат: "2020-01-01T10:00:00"
    - С миллисекундами: "2020-01-01T00:00:00.000000"
    - Только дата: "2020-01-01"

    Args:
        date_str (str): Строка с датой.

    Returns:
        datetime: Объект даты и времени.

    Raises:
        ValueError: Если формат даты не распознан.

    Examples:
        >>> _parse_date("2024-03-11")
        datetime.datetime(2024, 3, 11, 0, 0)

        >>> _parse_date("2024-03-11T12:34:56")
        datetime.datetime(2024, 3, 11, 12, 34, 56)

    Note:
        Функция приватная (начинается с _), используется только внутри модуля.
        Сначала пробуется встроенный fromisoformat(), затем резервные форматы.
    """
    # Попытка использовать встроенный парсер ISO
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        pass

    # Резервные форматы для нестандартных строк
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except Exception:
            continue

    raise ValueError(f"Invalid date format: {date_str}")


def sort_by_date(
    transactions: List[Dict[str, Any]], ascending: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Создает новый список с транзакциями, упорядоченными по полю "date".

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.
            Каждая транзакция должна содержать ключ "date".
        ascending (bool): Порядок сортировки:
            - True: по возрастанию (старые сначала)
            - False: по убыванию (новые сначала)
            По умолчанию True.

    Returns:
        List[Dict[str, Any]]: Новый отсортированный список транзакций.
            Исходный список не изменяется.

    Examples:
        >>> transactions = [
        ...     {"id": 1, "date": "2024-03-11"},
        ...     {"id": 2, "date": "2024-01-01"},
        ...     {"id": 3, "date": "2024-02-15"},
        ... ]
        >>> sort_by_date(transactions, ascending=True)
        [{'id': 2, 'date': '2024-01-01'},
         {'id': 3, 'date': '2024-02-15'},
         {'id': 1, 'date': '2024-03-11'}]

        >>> sort_by_date(transactions, ascending=False)  # Новые сначала
        [{'id': 1, 'date': '2024-03-11'},
         {'id': 3, 'date': '2024-02-15'},
         {'id': 2, 'date': '2024-01-01'}]

    Note:
        Функция создает новый список, не изменяя исходный.
        Это важно для сохранения исходных данных.
    """
    return sorted(
        transactions, key=lambda t: _parse_date(t["date"]), reverse=not ascending
    )


def filter_by_state(
    transactions: List[Dict[str, Any]], state: Optional[str]
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    Возвращает только транзакции с указанным статусом или
    управляет поведением при специальных значениях state.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.
        state (Optional[str]): Статус для фильтрации:
            - None: вернуть копию всего списка
            - "NONE": вернуть пустой список
            - "EXECUTED": только выполненные
            - "CANCELED": только отменённые
            - и другие статусы

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список транзакций.

    Examples:
        >>> transactions = [
        ...     {"id": 1, "state": "EXECUTED"},
        ...     {"id": 2, "state": "CANCELED"},
        ...     {"id": 3, "state": "EXECUTED"},
        ... ]

        >>> filter_by_state(transactions, "EXECUTED")
        [{'id': 1, 'state': 'EXECUTED'}, {'id': 3, 'state': 'EXECUTED'}]

        >>> filter_by_state(transactions, "CANCELED")
        [{'id': 2, 'state': 'CANCELED'}]

        >>> filter_by_state(transactions, None)  # Все транзакции
        [{'id': 1, 'state': 'EXECUTED'},
         {'id': 2, 'state': 'CANCELED'},
         {'id': 3, 'state': 'EXECUTED'}]

        >>> filter_by_state(transactions, "NONE")  # Пустой список
        []

    Note:
        - При state=None создается копия списка (без изменения исходного)
        - Транзакции без поля state не попадают в результат при фильтрации
    """
    if state is None:
        return list(transactions)  # Возвращаем копию
    if state == "NONE":
        return []  # Специальное значение для пустого результата
    return [t for t in transactions if t.get("state") == state]
