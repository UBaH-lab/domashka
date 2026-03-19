"""Тесты для модуля bank_utils.

Этот модуль содержит unit-тесты для функций поиска и категоризации транзакций.

Запуск тестов:
    pytest tests/test_bank_utils.py -v
"""

import pytest
from typing import List, Dict, Any

from bank_utils import process_bank_search, process_bank_operations


# ============================================================================
# ТЕСТЫ ДЛЯ process_bank_search
# ============================================================================


class TestProcessBankSearch:
    """Тесты для функции process_bank_search."""

    def test_search_single_match(self):
        """Тест поиска с одним совпадением."""
        data = [
            {"id": 1, "description": "Перевод денег"},
            {"id": 2, "description": "Оплата услуг"},
            {"id": 3, "description": "Снятие наличных"},
        ]

        result = process_bank_search(data, "перевод")

        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_search_multiple_matches(self):
        """Тест поиска с несколькими совпадениями."""
        data = [
            {"id": 1, "description": "Перевод на карту"},
            {"id": 2, "description": "перевод на счёт"},
            {"id": 3, "description": "Оплата"},
        ]

        result = process_bank_search(data, "перевод")

        assert len(result) == 2

    def test_search_case_insensitive(self):
        """Тест поиска без учёта регистра."""
        data = [
            {"id": 1, "description": "ПЕРЕВОД"},
            {"id": 2, "description": "перевод"},
            {"id": 3, "description": "Пе реВод"},
        ]

        result = process_bank_search(data, "перевод")

        assert len(result) == 2  # "ПЕРЕВОД" и "перевод"

    def test_search_partial_match(self):
        """Тест частичного совпадения."""
        data = [
            {"id": 1, "description": "Межбанковский перевод"},
        ]

        result = process_bank_search(data, "перевод")

        assert len(result) == 1

    def test_search_no_match(self):
        """Тест поиска без совпадений."""
        data = [
            {"id": 1, "description": "Оплата"},
            {"id": 2, "description": "Снятие"},
        ]

        result = process_bank_search(data, "перевод")

        assert result == []

    def test_search_empty_description(self):
        """Тест поиска с пустым описанием."""
        data = [
            {"id": 1, "description": ""},
            {"id": 2, "description": "Перевод"},
        ]

        result = process_bank_search(data, "перевод")

        assert len(result) == 1

    def test_search_special_characters(self):
        """Тест поиска со спецсимволами."""
        data = [
            {"id": 1, "description": "Перевод (срочный)"},
        ]

        result = process_bank_search(data, "(срочный)")

        assert len(result) == 1

    def test_search_empty_data(self):
        """Тест поиска в пустом списке."""
        result = process_bank_search([], "перевод")

        assert result == []

    def test_search_empty_query(self):
        """Тест поиска с пустым запросом (должен найти все)."""
        data = [
            {"id": 1, "description": "Перевод"},
            {"id": 2, "description": "Оплата"},
        ]

        result = process_bank_search(data, "")

        # Пустая строка найдётся везде
        assert len(result) == 2

    def test_search_missing_description_field(self):
        """Тест поиска при отсутствии поля description."""
        data = [
            {"id": 1, "amount": 1000},
            {"id": 2, "description": "Перевод"},
        ]

        result = process_bank_search(data, "перевод")

        assert len(result) == 1


# ============================================================================
# ТЕСТЫ ДЛЯ process_bank_operations
# ============================================================================


class TestProcessBankOperations:
    """Тесты для функции process_bank_operations."""

    def test_count_single_category(self):
        """Тест подсчёта одной категории."""
        data = [
            {"description": "Перевод на карту"},
            {"description": "Оплата услуг"},
            {"description": "перевод на счёт"},
        ]

        result = process_bank_operations(data, ["перевод"])

        assert result == {"перевод": 2}

    def test_count_multiple_categories(self):
        """Тест подсчёта нескольких категорий."""
        data = [
            {"description": "Перевод на карту"},
            {"description": "Оплата услуг"},
            {"description": "Снятие наличных"},
            {"description": "перевод"},
        ]

        result = process_bank_operations(data, ["перевод", "оплата", "снятие"])

        assert result["перевод"] == 2
        assert result["оплата"] == 1
        assert result["снятие"] == 1

    def test_count_case_insensitive(self):
        """Тест подсчёта без учёта регистра."""
        data = [
            {"description": "ПЕРЕВОД"},
            {"description": "перевод"},
            {"description": "Пе реВод"},
        ]

        result = process_bank_operations(data, ["перевод"])

        assert result["перевод"] == 2

    def test_count_no_matches(self):
        """Тест подсчёта без совпадений."""
        data = [
            {"description": "Оплата"},
            {"description": "Снятие"},
        ]

        result = process_bank_operations(data, ["перевод"])

        assert result["перевод"] == 0

    def test_count_overlapping_descriptions(self):
        """Тест когда одно описание содержит несколько категорий."""
        data = [
            {"description": "Перевод и оплата"},
        ]

        result = process_bank_operations(data, ["перевод", "оплата"])

        # Одно описание засчитывается в обе категории
        assert result["перевод"] == 1
        assert result["оплата"] == 1

    def test_count_empty_data(self):
        """Тест подсчёта в пустом списке."""
        result = process_bank_operations([], ["перевод", "оплата"])

        assert result == {"перевод": 0, "оплата": 0}

    def test_count_empty_categories(self):
        """Тест подсчёта с пустым списком категорий."""
        data = [
            {"description": "Перевод"},
        ]

        result = process_bank_operations(data, [])

        assert result == {}

    def test_count_missing_description(self):
        """Тест подсчёта при отсутствии поля description."""
        data = [
            {"id": 1, "amount": 1000},
            {"id": 2, "description": "Перевод"},
        ]

        result = process_bank_operations(data, ["перевод"])

        assert result["перевод"] == 1

    def test_count_preserves_category_order(self):
        """Тест сохранения порядка категорий."""
        data = [
            {"description": "Оплата и перевод"},
        ]

        result = process_bank_operations(data, ["перевод", "оплата", "снятие"])

        # Проверяем, что все категории есть в результате
        assert list(result.keys()) == ["перевод", "оплата", "снятие"]


# ============================================================================
# ФИКСТУРЫ
# ============================================================================


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с примерами транзакций для тестов."""
    return [
        {"id": 1, "description": "Перевод на карту"},
        {"id": 2, "description": "Оплата мобильной связи"},
        {"id": 3, "description": "Снятие наличных в банкомате"},
        {"id": 4, "description": "Перевод между счетами"},
        {"id": 5, "description": "Оплата коммунальных услуг"},
        {"id": 6, "description": "Покупка в магазине"},
    ]


# ============================================================================
# ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ
# ============================================================================


class TestParametrized:
    """Параметризованные тесты для проверки разных сценариев."""

    @pytest.mark.parametrize(
        "query,expected_count",
        [
            ("перевод", 2),
            ("оплата", 2),
            ("снятие", 1),
            ("магазин", 1),
            ("несуществующее", 0),
        ],
    )
    def test_search_various_queries(self, sample_transactions, query, expected_count):
        """Тест поиска с различными запросами."""
        result = process_bank_search(sample_transactions, query)
        assert len(result) == expected_count

    @pytest.mark.parametrize(
        "categories,expected",
        [
            (["перевод"], {"перевод": 2}),
            (["оплата", "снятие"], {"оплата": 2, "снятие": 1}),
            (["перевод", "оплата", "снятие"], {"перевод": 2, "оплата": 2, "снятие": 1}),
            (["несуществующее"], {"несуществующее": 0}),
        ],
    )
    def test_count_various_categories(self, sample_transactions, categories, expected):
        """Тест подсчёта с различными категориями."""
        result = process_bank_operations(sample_transactions, categories)
        assert result == expected
