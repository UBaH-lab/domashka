"""Модуль для чтения финансовых транзакций из файлов разных форматов.

Поддерживаемые форматы:
    - CSV (разделитель ';')
    - XLSX (Excel)

Пример использования:
    from src.transactions_reader import read_transactions_csv, read_transactions_excel

    data_csv = read_transactions_csv('data/transactions.csv')
    data_xlsx = read_transactions_excel('data/transactions.xlsx')
"""

from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd


def read_transactions_csv(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Читает транзакции из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу (разделитель ';').

    Returns:
        Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если файл пустой или повреждён.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    df = pd.read_csv(path, sep=";")

    if df.empty:
        raise ValueError("CSV-файл пустой")

    df = df.fillna("")
    return df.to_dict("records")


def read_transactions_excel(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Читает транзакции из Excel-файла (XLSX).

    Args:
        file_path: Путь к XLSX-файлу.

    Returns:
        Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если файл пустой или повреждён.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    df = pd.read_excel(path)

    if df.empty:
        raise ValueError("XLSX-файл пустой")

    df = df.fillna("")
    return df.to_dict("records")


def read_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Автоматически определяет формат и читает транзакции.

    Args:
        file_path: Путь к файлу (CSV или XLSX).

    Returns:
        Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если формат не поддерживается.
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".csv":
        return read_transactions_csv(path)
    elif ext in [".xlsx", ".xls"]:
        return read_transactions_excel(path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {ext}")
