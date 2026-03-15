"""
Тесты утилиты read_transactions_json из модуля src.utils.

Цель:
- проверить корректное чтение валидного списка словарей.
- вернуть пустой список, если файл пуст, не список, не найден или содержит неверный JSON.
"""

import json

from src.utils import read_transactions_json


def test_read_transactions_valid(tmp_path):
    """Проверка чтения валидного JSON, содержащего список словарей."""
    data = [{"id": 1, "amount": 10, "currency": "USD"}]
    p = tmp_path / "ops.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    assert read_transactions_json(str(p)) == data


def test_read_transactions_empty(tmp_path):
    """Проверка файла, содержащего пустой список ([])."""
    p = tmp_path / "empty.json"
    p.write_text("[]", encoding="utf-8")
    assert read_transactions_json(str(p)) == []


def test_read_transactions_not_list(tmp_path):
    """Проверка файла, где верхний уровень не является списком (словарь)."""
    p = tmp_path / "not_list.json"
    p.write_text(json.dumps({"a": 1}), encoding="utf-8")
    assert read_transactions_json(str(p)) == []


def test_read_transactions_not_found(tmp_path):
    """Проверка поведения при отсутствии файла -> возвращает []."""
    assert read_transactions_json(str(tmp_path / "missing.json")) == []
