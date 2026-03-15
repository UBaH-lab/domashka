"""
Тесты для модуля src.external_api: конвертация валют в рубли.

Проверяются:
- конвертация RUB без изменений;
- конвертация USD/EUR с использованием внешнего API через requests.get (mock).
Мокируются запросы и устанавливается переменная окружения EXCHANGE_API_KEY.
"""

from unittest.mock import patch

from src.external_api import convert_to_rubles


def test_convert_to_rubles_rub(monkeypatch):
    """Проверка конвертации валюты RUB: сумма возвращается без изменений."""
    txn = {"amount": 123.4, "currency": "RUB"}
    assert convert_to_rubles(txn) == 123.4


@patch("src.external_api.requests.get")
def test_convert_to_rubles_usd(mock_get, monkeypatch):
    """Проверка конвертации USD: курс берётся через API и применяется к сумме."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"RUB": 75.5}}
    mock_get.return_value.raise_for_status = lambda: None
    txn = {"amount": 10.0, "currency": "USD"}
    monkeypatch.setenv("EXCHANGE_API_KEY", "testkey")
    assert abs(convert_to_rubles(txn) - 755.0) < 1e-6


@patch("src.external_api.requests.get")
def test_convert_to_rubles_eur(mock_get, monkeypatch):
    """Проверка конвертации EUR: аналогично USD."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"RUB": 90.0}}
    mock_get.return_value.raise_for_status = lambda: None
    txn = {"amount": 20.0, "currency": "EUR"}
    monkeypatch.setenv("EXCHANGE_API_KEY", "testkey")
    assert abs(convert_to_rubles(txn) - 1800.0) < 1e-6
