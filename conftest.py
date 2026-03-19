"""Общие фикстуры для всех тестов.

Этот модуль содержит фикстуры pytest, доступные во всех тестовых файлах.

Расположение: tests/conftest.py (или в корне проекта)
"""

import pytest
from typing import List, Dict, Any


@pytest.fixture
def sample_json_data() -> List[Dict[str, Any]]:
    """Фикстура с примером данных в JSON-формате."""
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "14.10.2018",
            "operationAmount": {
                "amount": "30164.00",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "23.12.2019",
            "operationAmount": {
                "amount": "29852.82",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]


@pytest.fixture
def sample_csv_data() -> List[Dict[str, Any]]:
    """Фикстура с примером данных в CSV-формате."""
    return [
        {
            "date": "01.01.2024",
            "amount": 1000,
            "currency": "RUB",
            "description": "Перевод",
            "status": "EXECUTED",
        },
        {
            "date": "02.01.2024",
            "amount": 2000,
            "currency": "USD",
            "description": "Оплата",
            "status": "CANCELED",
        },
    ]
