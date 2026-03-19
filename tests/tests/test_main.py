"""Тесты для модуля main.

Этот модуль содержит unit-тесты для всех функций работы с транзакциями.
Использует pytest и unittest.mock для изоляции тестов.

Запуск тестов:
    pytest tests/test_main.py -v
    pytest tests/test_main.py --cov=main --cov-report=term-missing
"""

import json
import pytest
from unittest.mock import patch
from typing import List, Dict, Any

from main import (
    load_transactions_from_json,
    load_transactions_from_csv,
    load_transactions_from_excel,
    get_valid_status,
    filter_by_status,
    sort_by_date,
    filter_by_currency,
    mask_number,
    format_transaction,
    ask_yes_no,
)


# ============================================================================
# ТЕСТЫ ДЛЯ load_transactions_from_json
# ============================================================================


class TestLoadTransactionsFromJson:
    """Тесты для функции load_transactions_from_json."""

    def test_load_valid_json(self, tmp_path):
        """Тест успешной загрузки JSON-файла."""
        # Подготовка тестовых данных
        test_data = [
            {"id": 1, "date": "01.01.2024", "amount": 1000},
            {"id": 2, "date": "02.01.2024", "amount": 2000},
        ]

        # Создаём временный JSON-файл
        json_file = tmp_path / "test.json"
        json_file.write_text(
            json.dumps(test_data, ensure_ascii=False), encoding="utf-8"
        )

        # Выполняем тест
        result = load_transactions_from_json(str(json_file))

        # Проверяем результат
        assert result == test_data
        assert len(result) == 2

    def test_load_empty_json(self, tmp_path):
        """Тест загрузки пустого JSON-файла."""
        json_file = tmp_path / "empty.json"
        json_file.write_text("[]", encoding="utf-8")

        result = load_transactions_from_json(str(json_file))

        assert result == []

    def test_file_not_found(self, capsys):
        """Тест обработки отсутствующего файла."""
        result = load_transactions_from_json("nonexistent.json")

        assert result == []
        captured = capsys.readouterr()
        assert "не найден" in captured.out

    def test_invalid_json(self, tmp_path, capsys):
        """Тест обработки некорректного JSON."""
        json_file = tmp_path / "invalid.json"
        json_file.write_text("{invalid json}", encoding="utf-8")

        result = load_transactions_from_json(str(json_file))

        assert result == []
        captured = capsys.readouterr()
        assert "Ошибка" in captured.out

    def test_load_json_with_cyrillic(self, tmp_path):
        """Тест загрузки JSON с кириллицей."""
        test_data = [
            {"description": "Перевод на счёт", "amount": 1500},
        ]

        json_file = tmp_path / "cyrillic.json"
        json_file.write_text(
            json.dumps(test_data, ensure_ascii=False), encoding="utf-8"
        )

        result = load_transactions_from_json(str(json_file))

        assert result[0]["description"] == "Перевод на счёт"


# ============================================================================
# ТЕСТЫ ДЛЯ load_transactions_from_csv
# ============================================================================


class TestLoadTransactionsFromCsv:
    """Тесты для функции load_transactions_from_csv."""

    @patch("main.read_transactions_csv")
    def test_load_valid_csv(self, mock_read, tmp_path):
        """Тест успешной загрузки CSV-файла."""
        mock_data = [
            {"date": "01.01.2024", "amount": 1000},
            {"date": "02.01.2024", "amount": 2000},
        ]
        mock_read.return_value = mock_data

        csv_file = tmp_path / "test.csv"
        csv_file.write_text("date,amount\n01.01.2024,1000", encoding="utf-8")

        result = load_transactions_from_csv(str(csv_file))

        assert result == mock_data
        assert len(result) == 2

    @patch("main.read_transactions_csv")
    def test_load_empty_csv(self, mock_read):
        """Тест загрузки пустого CSV-файла."""
        mock_read.return_value = []

        result = load_transactions_from_csv("empty.csv")

        assert result == []

    @patch("main.read_transactions_csv", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_read, capsys):
        """Тест обработки отсутствующего CSV-файла."""
        result = load_transactions_from_csv("nonexistent.csv")

        assert result == []
        captured = capsys.readouterr()
        assert "не найден" in captured.out

    @patch("main.read_transactions_csv", side_effect=ValueError("Пустой файл"))
    def test_invalid_csv(self, mock_read, capsys):
        """Тест обработки некорректного CSV."""
        result = load_transactions_from_csv("invalid.csv")

        assert result == []
        captured = capsys.readouterr()
        assert "Пустой файл" in captured.out


# ============================================================================
# ТЕСТЫ ДЛЯ load_transactions_from_excel
# ============================================================================


class TestLoadTransactionsFromExcel:
    """Тесты для функции load_transactions_from_excel."""

    @patch("main.read_transactions_excel")
    def test_load_valid_excel(self, mock_read):
        """Тест успешной загрузки XLSX-файла."""
        mock_data = [
            {"date": "01.01.2024", "amount": 1000},
        ]
        mock_read.return_value = mock_data

        result = load_transactions_from_excel("test.xlsx")

        assert result == mock_data

    @patch("main.read_transactions_excel", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_read, capsys):
        """Тест обработки отсутствующего XLSX-файла."""
        result = load_transactions_from_excel("nonexistent.xlsx")

        assert result == []
        captured = capsys.readouterr()
        assert "не найден" in captured.out

    @patch("main.read_transactions_excel", side_effect=ValueError("Ошибка формата"))
    def test_invalid_excel(self, mock_read, capsys):
        """Тест обработки некорректного XLSX."""
        result = load_transactions_from_excel("invalid.xlsx")

        assert result == []
        captured = capsys.readouterr()
        assert "Ошибка формата" in captured.out


# ============================================================================
# ТЕСТЫ ДЛЯ get_valid_status
# ============================================================================


class TestGetValidStatus:
    """Тесты для функции get_valid_status."""

    @patch("builtins.input", return_value="EXECUTED")
    def test_valid_status_executed(self, mock_input, capsys):
        """Тест ввода корректного статуса EXECUTED."""
        result = get_valid_status()

        assert result == "EXECUTED"

    @patch("builtins.input", return_value="canceled")
    def test_valid_status_lowercase(self, mock_input):
        """Тест ввода статуса в нижнем регистре."""
        result = get_valid_status()

        assert result == "CANCELED"

    @patch("builtins.input", side_effect=["invalid", "PENDING"])
    def test_invalid_then_valid_status(self, mock_input, capsys):
        """Тест повторного ввода при некорректном статусе."""
        result = get_valid_status()

        assert result == "PENDING"
        captured = capsys.readouterr()
        assert "недоступен" in captured.out

    @patch("builtins.input", side_effect=["executed", "EXECUTED"])
    def test_status_with_spaces(self, mock_input):
        """Тест ввода статуса с пробелами."""
        result = get_valid_status()

        assert result == "EXECUTED"


# ============================================================================
# ТЕСТЫ ДЛЯ filter_by_status
# ============================================================================


class TestFilterByStatus:
    """Тесты для функции filter_by_status."""

    def test_filter_executed(self):
        """Тест фильтрации по статусу EXECUTED."""
        data = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "CANCELED"},
            {"id": 3, "state": "EXECUTED"},
        ]

        result = filter_by_status(data, "EXECUTED")

        assert len(result) == 2
        assert all(item["state"] == "EXECUTED" for item in result)

    def test_filter_canceled(self):
        """Тест фильтрации по статусу CANCELED."""
        data = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "CANCELED"},
        ]

        result = filter_by_status(data, "CANCELED")

        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_with_status_field(self):
        """Тест фильтрации с полем 'status' вместо 'state'."""
        data = [
            {"id": 1, "status": "PENDING"},
            {"id": 2, "state": "PENDING"},
        ]

        result = filter_by_status(data, "PENDING")

        assert len(result) == 2

    def test_filter_no_match(self):
        """Тест когда нет подходящих транзакций."""
        data = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "CANCELED"},
        ]

        result = filter_by_status(data, "PENDING")

        assert result == []

    def test_filter_case_insensitive(self):
        """Тест нечувствительности к регистру."""
        data = [
            {"id": 1, "state": "executed"},
            {"id": 2, "state": "Executed"},
        ]

        result = filter_by_status(data, "EXECUTED")

        assert len(result) == 2

    def test_filter_empty_data(self):
        """Тест фильтрации пустого списка."""
        result = filter_by_status([], "EXECUTED")

        assert result == []


# ============================================================================
# ТЕСТЫ ДЛЯ sort_by_date
# ============================================================================


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_descending(self):
        """Тест сортировки по убыванию (по умолчанию)."""
        data = [
            {"date": "15.06.2024", "id": 2},
            {"date": "01.01.2024", "id": 1},
            {"date": "31.12.2024", "id": 3},
        ]

        result = sort_by_date(data)

        assert result[0]["id"] == 3  # 31.12.2024
        assert result[1]["id"] == 2  # 15.06.2024
        assert result[2]["id"] == 1  # 01.01.2024

    def test_sort_ascending(self):
        """Тест сортировки по возрастанию."""
        data = [
            {"date": "15.06.2024", "id": 2},
            {"date": "01.01.2024", "id": 1},
            {"date": "31.12.2024", "id": 3},
        ]

        result = sort_by_date(data, ascending=True)

        assert result[0]["id"] == 1  # 01.01.2024
        assert result[1]["id"] == 2  # 15.06.2024
        assert result[2]["id"] == 3  # 31.12.2024

    def test_sort_same_dates(self):
        """Тест сортировки с одинаковыми датами."""
        data = [
            {"date": "01.01.2024", "id": 1},
            {"date": "01.01.2024", "id": 2},
        ]

        result = sort_by_date(data)

        assert len(result) == 2

    def test_sort_missing_date(self):
        """Тест сортировки с отсутствующей датой."""
        data = [
            {"date": "01.01.2024", "id": 1},
            {"date": "", "id": 2},
            {"date": "31.12.2024", "id": 3},
        ]

        result = sort_by_date(data, ascending=True)

        # Пустая дата должна быть в начале при возрастании
        assert result[0]["id"] == 2
        assert result[-1]["id"] == 3

    def test_sort_empty_list(self):
        """Тест сортировки пустого списка."""
        result = sort_by_date([])

        assert result == []


# ============================================================================
# ТЕСТЫ ДЛЯ filter_by_currency
# ============================================================================


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_rub_json_format(self):
        """Тест фильтрации RUB в формате JSON."""
        data = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
        ]

        result = filter_by_currency(data, "RUB")

        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_filter_usd(self):
        """Тест фильтрации USD."""
        data = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
        ]

        result = filter_by_currency(data, "USD")

        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_simple_currency_field(self):
        """Тест фильтрации с простым полем currency."""
        data = [
            {"id": 1, "currency": "RUB"},
            {"id": 2, "currency": "EUR"},
        ]

        result = filter_by_currency(data, "RUB")

        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_filter_no_match(self):
        """Тест когда нет транзакций в указанной валюте."""
        data = [
            {"id": 1, "currency": "USD"},
            {"id": 2, "currency": "EUR"},
        ]

        result = filter_by_currency(data, "RUB")

        assert result == []

    def test_filter_empty_data(self):
        """Тест фильтрации пустого списка."""
        result = filter_by_currency([], "RUB")

        assert result == []


# ============================================================================
# ТЕСТЫ ДЛЯ mask_number
# ============================================================================


class TestMaskNumber:
    """Тесты для функции mask_number."""

    @patch("main.get_mask_card_number")
    def test_mask_card_number(self, mock_mask):
        """Тест маскировки номера карты (16 цифр)."""
        mock_mask.return_value = "1234 56** **** 3456"

        result = mask_number("1234567890123456")

        mock_mask.assert_called_once_with("1234567890123456")
        assert result == "1234 56** **** 3456"

    @patch("main.get_mask_card_number")
    def test_mask_card_with_spaces(self, mock_mask):
        """Тест маскировки номера карты с пробелами."""
        mock_mask.return_value = "1234 56** **** 3456"

        result = mask_number("1234 5678 9012 3456")

        # Пробелы должны быть удалены перед маскировкой
        mock_mask.assert_called_once_with("1234567890123456")
        assert result == "1234 56** **** 3456"

    def test_mask_account_number(self):
        """Тест маскировки номера счёта (>16 цифр)."""
        result = mask_number("12345678901234567890")

        assert result == "**7890"

    def test_mask_account_with_prefix(self):
        """Тест маскировки счёта с текстовым префиксом."""
        result = mask_number("Счёт 12345678901234567890")

        assert result == "**7890"

    def test_mask_empty_string(self):
        """Тест маскировки пустой строки."""
        result = mask_number("")

        assert result == ""

    def test_mask_short_number(self):
        """Тест маскировки короткого номера (<16 цифр)."""
        result = mask_number("12345678")

        # Короткие номера возвращаются как есть
        assert result == "12345678"


# ============================================================================
# ТЕСТЫ ДЛЯ format_transaction
# ============================================================================


class TestFormatTransaction:
    """Тесты для функции format_transaction."""

    def test_format_full_transaction(self):
        """Тест форматирования полной транзакции."""
        transaction = {
            "date": "15.06.2024",
            "description": "Перевод",
            "from": "Счёт 12345678901234567890",
            "to": "Карта 1234567890123456",
            "operationAmount": {"amount": 1000, "currency": {"code": "RUB"}},
        }

        result = format_transaction(transaction)

        assert "15.06.2024" in result
        assert "Перевод" in result
        assert "->" in result
        assert "1000" in result
        assert "руб." in result

    def test_format_transaction_without_from(self):
        """Тест форматирования транзакции без отправителя."""
        transaction = {
            "date": "01.01.2024",
            "description": "Пополнение",
            "to": "Карта 1234567890123456",
            "operationAmount": {"amount": 500, "currency": {"code": "USD"}},
        }

        result = format_transaction(transaction)

        assert "Пополнение" in result
        assert "->" not in result
        assert "USD" in result

    def test_format_transaction_simple_format(self):
        """Тест форматирования транзакции в простом формате."""
        transaction = {
            "date": "01.01.2024",
            "description": "Оплата",
            "to": "Магазин",
            "amount": 2000,
            "currency": "RUB",
        }

        result = format_transaction(transaction)

        assert "Оплата" in result
        assert "2000" in result
        assert "руб." in result

    def test_format_transaction_empty_fields(self):
        """Тест форматирования транзакции с пустыми полями."""
        transaction = {
            "date": "",
            "description": "",
            "to": "",
            "amount": 0,
        }

        result = format_transaction(transaction)

        # Должна быть строка суммы
        assert "Сумма:" in result


# ============================================================================
# ТЕСТЫ ДЛЯ ask_yes_no
# ============================================================================


class TestAskYesNo:
    """Тесты для функции ask_yes_no."""

    @patch("builtins.input", return_value="да")
    def test_yes_response_da(self, mock_input, capsys):
        """Тест ответа 'да'."""
        result = ask_yes_no("Продолжить?")

        assert result is True

    @patch("builtins.input", return_value="yes")
    def test_yes_response_yes(self, mock_input):
        """Тест ответа 'yes'."""
        result = ask_yes_no("Continue?")

        assert result is True

    @patch("builtins.input", return_value="y")
    def test_yes_response_y(self, mock_input):
        """Тест ответа 'y'."""
        result = ask_yes_no("Save?")

        assert result is True

    @patch("builtins.input", return_value="д")
    def test_yes_response_d(self, mock_input):
        """Тест ответа 'д'."""
        result = ask_yes_no("Подтвердить?")

        assert result is True

    @patch("builtins.input", return_value="нет")
    def test_no_response_net(self, mock_input):
        """Тест ответа 'нет'."""
        result = ask_yes_no("Продолжить?")

        assert result is False

    @patch("builtins.input", return_value="no")
    def test_no_response_no(self, mock_input):
        """Тест ответа 'no'."""
        result = ask_yes_no("Continue?")

        assert result is False

    @patch("builtins.input", return_value="ДА")
    def test_uppercase_response(self, mock_input):
        """Тест ответа в верхнем регистре."""
        result = ask_yes_no("Продолжить?")

        assert result is True

    @patch("builtins.input", return_value="  да  ")
    def test_response_with_spaces(self, mock_input):
        """Тест ответа с пробелами."""
        result = ask_yes_no("Продолжить?")

        assert result is True


# ============================================================================
# ФИКСТУРЫ
# ============================================================================


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с примерами транзакций для тестов."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "01.01.2024",
            "amount": 1000,
            "currency": "RUB",
            "description": "Перевод",
            "from": "Счёт 12345678901234567890",
            "to": "Карта 1234567890123456",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "15.06.2024",
            "amount": 2000,
            "currency": "USD",
            "description": "Оплата услуг",
            "to": "Компания ABC",
        },
        {
            "id": 3,
            "state": "PENDING",
            "date": "31.12.2024",
            "amount": 500,
            "currency": "RUB",
            "description": "Пополнение счёта",
        },
    ]


# ============================================================================
# ИНТЕГРАЦИОННЫЕ ТЕСТЫ
# ============================================================================


class TestIntegration:
    """Интеграционные тесты для цепочек функций."""

    def test_filter_and_sort(self, sample_transactions):
        """Тест цепочки фильтрации и сортировки."""
        # Фильтруем по статусу
        filtered = filter_by_status(sample_transactions, "EXECUTED")

        # Сортируем по дате
        sorted_data = sort_by_date(filtered, ascending=True)

        assert len(sorted_data) == 1
        assert sorted_data[0]["id"] == 1

    def test_multiple_filters(self, sample_transactions):
        """Тест применения нескольких фильтров подряд."""
        # Фильтруем по статусу
        result = filter_by_status(sample_transactions, "EXECUTED")

        # Фильтруем по валюте
        result = filter_by_currency(result, "RUB")

        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_empty_result_chain(self, sample_transactions):
        """Тест цепочки, приводящей к пустому результату."""
        # Фильтруем по статусу EXECUTED
        result = filter_by_status(sample_transactions, "EXECUTED")

        # Фильтруем по валюте USD (не совпадает)
        result = filter_by_currency(result, "USD")

        assert result == []
