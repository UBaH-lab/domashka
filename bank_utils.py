"""Утилиты для обработки банковских транзакций."""

from typing import Any, Dict, List
import re
from collections import Counter


def process_bank_search(
    data: List[Dict[str, Any]], search: str
) -> List[Dict[str, Any]]:
    """Возвращает транзакции, у которых в поле description встречается строка search.

    Args:
        data: Список словарей с транзакциями.
        search: Строка для поиска.

    Returns:
        Список транзакций, удовлетворяющих условию.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result: List[Dict[str, Any]] = []
    for item in data:
        description = str(item.get("description", ""))
        if pattern.search(description):
            result.append(item)
    return result


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """Подсчитывает количество операций по категориям.

    Args:
        data: Список транзакций.
        categories: Список категорий для подсчета.

    Returns:
        Словарь с количеством операций по категориям.
    """
    counts = Counter({cat: 0 for cat in categories})
    for item in data:
        desc = str(item.get("description", ""))
        for cat in categories:
            if re.search(re.escape(cat), desc, re.IGNORECASE):
                counts[cat] += 1
    return dict(counts)
