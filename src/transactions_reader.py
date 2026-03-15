"""Модуль для чтения финансовых транзакций из CSV и Excel файлов."""

from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd


def read_transactions_csv(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Считывает финансовые транзакции из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        Список словарей с данными транзакций

    Raises:
        FileNotFoundError: Если файл не существует
        ValueError: Если файл пустой или имеет неверный формат
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    try:
        df = pd.read_csv(path)

        if df.empty:
            raise ValueError("Файл пустой")

        transactions = df.to_dict("records")

        return transactions

    except pd.errors.EmptyDataError:
        raise ValueError("Файл пустой или имеет неверный формат")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV-файла: {e}")


def read_transactions_excel(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Считывает финансовые транзакции из XLSX-файла.

    Args:
        file_path: Путь к XLSX-файлу

    Returns:
        Список словарей с данными транзакций

    Raises:
        FileNotFoundError: Если файл не существует
        ValueError: Если файл пустой или имеет неверный формат
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    try:
        df = pd.read_excel(path)

        if df.empty:
            raise ValueError("Файл пустой")

        transactions = df.to_dict("records")

        return transactions

    except Exception as e:
        raise ValueError(f"Ошибка при чтении XLSX-файла: {e}")


def read_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Универсальная функция для чтения транзакций из файла.
    Автоматически определяет формат по расширению файла.

    Args:
        file_path: Путь к файлу (CSV или XLSX)

    Returns:
        Список словарей с данными транзакций

    Raises:
        ValueError: Если формат файла не поддерживается
    """
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".csv":
        return read_transactions_csv(path)
    elif extension in [".xlsx", ".xls"]:
        return read_transactions_excel(path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {extension}")
