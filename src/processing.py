from datetime import datetime
from typing import Any, Dict, List, Optional


def _parse_date(date_str: str) -> datetime:
    """
    Преобразование даты из строки в datetime.
    Поддерживает форматы:
      - ISO: 2020-01-01T10:00:00
      - 2020-01-01T00:00:00.000000 (с.ms)
      - 2020-01-01
    Если формат не распознаётся, возбуждает ValueError.
    """
    # Попытка использовать встроенный парсер ISO
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        pass

    # Резервные форматы
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
    Возвращает новый список транзакций, отсортированный по полю 'date'.
    - ascending True: oldest first
    - ascending False: newest first
    """
    return sorted(
        transactions, key=lambda t: _parse_date(t["date"]), reverse=not ascending
    )


def filter_by_state(
    transactions: List[Dict[str, Any]], state: Optional[str]
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по полю 'state'.
    - state is None: вернуть копию исходного списка
    - state == "NONE": вернуть пустой список
    - иначе: вернуть только те транзакции, где t["state"] == state
    """
    if state is None:
        return list(transactions)
    if state == "NONE":
        return []
    return [t for t in transactions if t.get("state") == state]
