"""
Модуль utils содержит утилиты для работы с JSON-файлами операций.

Функции:
- read_transactions_json(path: str) -> List[Dict[str, Any]]
  Читает файл JSON по заданному пути и возвращает список словарей с данными
  о финансовых операциях. Если файл не найден, содержит неверный JSON или
  не является списком — возвращает пустой список.
"""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def read_transactions_json(path: str) -> List[Dict[str, Any]]:
    """Прочитать JSON-файл с операциями и вернуть список словарей.

    Параметры:
    - path: строка, путь к JSON-файлу

    Возвращает:
    - list[dict]: список словарей, если содержимое файла является списком.
    - пустой список: если файл не найден, пустой или содержит неверный JSON.
    """
    logger.info(f"Попытка чтения файла: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.warning(f"Файл не найден: {path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON в файле {path}: {e}")
        return []

    if not isinstance(data, list):
        logger.warning(f"Файл {path} не содержит список на верхнем уровне")
        return []

    logger.info(f"Успешно прочитано {len(data)} операций из {path}")
    return data


__all__ = ["read_transactions_json"]
