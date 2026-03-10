"""
Модуль utils содержит утилиты для работы с JSON-файлами операций.

Функции:
- read_transactions_json(path: str) -> List[Dict[str, Any]]
  Читает файл JSON по заданному пути и возвращает список словарей с данными
  о финансовых операциях. Если файл не найден, содержит неверный JSON или
  не является списком — возвращает пустой список.

Пример использования:
data = read_transactions_json("data/operations.json")
"""

from typing import List, Dict, Any
import json


def read_transactions_json(path: str) -> List[Dict[str, Any]]:
    """Прочитать JSON-файл с операциями и вернуть список словарей.

    Параметры:
    - path: строка, путь к JSON-файлу, который должен содержать список объектов
      словарей с данными о финансовых операциях.

    Возвращает:
    - list[dict]: список словарей, если содержимое файла является списком.
    - пустой список: если файл не найден, пустой, не является списком
      или содержит неверный JSON.

    Примечания:
    - Если JSON валиден, но верхний уровень не является списком, возвращается [].
    - Исключения внутри чтения обрабатываются и приводят к возвращению [].
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return data if isinstance(data, list) else []


__all__ = ["read_transactions_json"]
