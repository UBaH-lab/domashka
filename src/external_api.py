"""
Модуль external_api реализует конвертацию валют в рубли c использованием внешнего API.

Функции:
- _get_api_key() -> str
  Возвращает API-ключ, взятый из переменной окружения EXCHANGE_API_KEY.
  При отсутствии ключа поднимает RuntimeError.

- convert_to_rubles(transaction: Dict[str, Any]) -> float
  Конвертирует сумму транзакции в рубли.
  Параметры транзакции (словарь) должны содержать:
  - "amount": числовое значение суммы
  - "currency": строка, одна из {"RUB", "USD", "EUR"}

  Логика:
  - если currency == "RUB" — возвращает amount
  - если currency в {"USD", "EUR"} — делает запрос к API курсов
    и умножает amount на курс к RUB
  - иначе — возбуждает ValueError

  При конвертации USD/EUR нужен действующий API-ключ в переменной окружения.
  Результат возвращается как float.
"""

from typing import Dict, Any
import os
import requests


def _get_api_key() -> str:
    """Получить API-ключ из окружения.

    Возвращает:
    - строку с API-ключом.

    Исключения:
    - RuntimeError, если переменная окружения EXCHANGE_API_KEY не найдена.
    """
    key = os.environ.get("EXCHANGE_API_KEY")
    if not key:
        raise RuntimeError("Missing EXCHANGE_API_KEY in environment")
    return key


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертировать сумму транзакции в рубли.

    Параметры:
    - transaction: словарь с данными о транзакции. Ожидаются ключи:
        - "amount": числовое значение суммы (float|int)
        - "currency": строка, одна из {"RUB", "USD", "EUR"}

    Возвращает:
    - float: сумма транзакции в рублях.

    Логика:
    - если currency == "RUB": вернуть amount
    - если currency == "USD" или "EUR": обратиться к внешнему API
      и умножить на курс RUB (курс берётся из ответа API)

    Исключения:
    - ValueError, если валюта не поддерживается или курс не найден
    - RuntimeError, если отсутствует API-ключ

    Пример вызова:
    convert_to_rubles({"amount": 10, "currency": "USD"})
    """
    amount = float(transaction.get("amount", 0.0))
    currency = str(transaction.get("currency", "RUB")).upper()

    if currency == "RUB":
        return amount

    if currency in ("USD", "EUR"):
        api_key = _get_api_key()
        url = "https://api.apilayer.com/exchangerates_data/latest"
        headers = {"apikey": api_key}
        params = {"base": currency, "symbols": "RUB"}

        resp = requests.get(url, headers=headers, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        rate = data.get("rates", {}).get("RUB")
        if rate is None:
            raise ValueError("Rate not found in API response")
        return float(amount) * float(rate)

    raise ValueError(f"Unsupported currency: {currency}")


__all__ = ["convert_to_rubles"]
