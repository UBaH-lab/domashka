from typing import List, Dict, Generator, Iterator


def filter_by_currency(transactions: List[Dict], currency_code: str) -> Iterator[Dict]:
    """
    Возвращает итератор, по которому выдаются транзакции, валютой которых является `currency_code`.
    """
    for transaction in transactions:
        # Получаем название валюты (или code)
        transaction_currency = transaction["operationAmount"]["currency"]["code"]
        if transaction_currency == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """
    Генератор, возвращающий описание каждой транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int = 1, end: int = 9999999999999999) -> Generator[str, None, None]:
    """
    Генератор номеров карт в формате XXXX XXXX XXXX XXXX.
    Начинается с `start` и идет до `end` включительно.
    """
    for number in range(start, end + 1):
        # Форматировать число в 16-значный формат с ведущими нулями
        card_number = f"{number:016d}"  # 16 цифр, с ведущими нулями
        # Разбить на группы по 4
        formatted = ' '.join(card_number[i:i+4] for i in range(0, 16, 4))
        yield formatted