"""Тесты для модуля чтения транзакций."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.transactions_reader import (
    read_transactions,
    read_transactions_csv,
    read_transactions_excel,
)


class TestReadTransactionsCSV:
    """Тесты для функции read_transactions_csv."""

    @patch("src.transactions_reader.Path")
    @patch("src.transactions_reader.pd.read_csv")
    def test_read_csv_success(self, mock_read_csv, mock_path):
        """Тест успешного чтения CSV-файла."""
        # Настройка моков
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        # Создаём тестовый DataFrame
        test_data = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "amount": [100.0, 200.0, 300.0],
                "category": ["food", "transport", "entertainment"],
            }
        )
        mock_read_csv.return_value = test_data

        # Вызываем функцию
        transactions = read_transactions_csv("test.csv")

        # Проверяем результат
        assert len(transactions) == 3
        assert transactions[0]["id"] == 1
        assert transactions[0]["amount"] == 100.0
        assert transactions[0]["category"] == "food"

        # Проверяем, что read_csv был вызван с правильным аргументом
        mock_read_csv.assert_called_once()

    @patch("src.transactions_reader.Path")
    def test_read_csv_file_not_found(self, mock_path):
        """Тест обработки несуществующего файла."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance

        with pytest.raises(FileNotFoundError, match="Файл test.csv не найден"):
            read_transactions_csv("test.csv")

    @patch("src.transactions_reader.Path")
    @patch("src.transactions_reader.pd.read_csv")
    def test_read_csv_empty_file(self, mock_read_csv, mock_path):
        """Тест обработки пустого CSV-файла."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_read_csv.return_value = pd.DataFrame()

        with pytest.raises(ValueError, match="Файл пустой"):
            read_transactions_csv("test.csv")

    @patch("src.transactions_reader.Path")
    @patch("src.transactions_reader.pd.read_csv")
    def test_read_csv_invalid_format(self, mock_read_csv, mock_path):
        """Тест обработки файла с неверным форматом."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_read_csv.side_effect = pd.errors.EmptyDataError()

        with pytest.raises(ValueError, match="Файл пустой или имеет неверный формат"):
            read_transactions_csv("test.csv")


class TestReadTransactionsExcel:
    """Тесты для функции read_transactions_excel."""

    @patch("src.transactions_reader.Path")
    @patch("src.transactions_reader.pd.read_excel")
    def test_read_excel_success(self, mock_read_excel, mock_path):
        """Тест успешного чтения XLSX-файла."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        test_data = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "amount": [100.0, 200.0, 300.0],
                "category": ["food", "transport", "entertainment"],
            }
        )
        mock_read_excel.return_value = test_data

        transactions = read_transactions_excel("test.xlsx")

        assert len(transactions) == 3
        assert transactions[0]["id"] == 1
        assert transactions[0]["amount"] == 100.0
        assert transactions[0]["category"] == "food"

        mock_read_excel.assert_called_once()

    @patch("src.transactions_reader.Path")
    def test_read_excel_file_not_found(self, mock_path):
        """Тест обработки несуществующего файла."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance

        with pytest.raises(FileNotFoundError, match="Файл test.xlsx не найден"):
            read_transactions_excel("test.xlsx")

    @patch("src.transactions_reader.Path")
    @patch("src.transactions_reader.pd.read_excel")
    def test_read_excel_empty_file(self, mock_read_excel, mock_path):
        """Тест обработки пустого XLSX-файла."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_read_excel.return_value = pd.DataFrame()

        with pytest.raises(ValueError, match="Файл пустой"):
            read_transactions_excel("test.xlsx")


class TestReadTransactions:
    """Тесты для универсальной функции read_transactions."""

    @patch("src.transactions_reader.read_transactions_csv")
    def test_read_csv_auto(self, mock_read_csv):
        """Тест автоматического определения CSV-формата."""
        mock_read_csv.return_value = [{"id": 1, "amount": 100.0, "category": "food"}]

        transactions = read_transactions("test.csv")

        assert len(transactions) == 1
        mock_read_csv.assert_called_once()

    @patch("src.transactions_reader.read_transactions_excel")
    def test_read_excel_auto(self, mock_read_excel):
        """Тест автоматического определения XLSX-формата."""
        mock_read_excel.return_value = [{"id": 1, "amount": 100.0, "category": "food"}]

        transactions = read_transactions("test.xlsx")

        assert len(transactions) == 1
        mock_read_excel.assert_called_once()

    def test_unsupported_format(self):
        """Тест обработки неподдерживаемого формата."""
        with pytest.raises(ValueError, match="Неподдерживаемый формат файла"):
            read_transactions("test.txt")
