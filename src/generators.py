from typing import Dict, Generator, List


def filter_by_currency(
    transactions: List[Dict], currency_code: str
) -> Generator[Dict, None, None]:
    """
    Проходит по списку транзакций и возвращает только те,
    у которых валюта совпадает с указанным кодом.
    """
    for transaction in transactions:
        currency = transaction["operationAmount"]["currency"]["code"]
        if currency == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """
    Генератор, который возвращает описание каждой транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(
    start: int = 1, stop: int = 9999999999999999
) -> Generator[str, None, None]:
    """
    Генератор номеров карт в формате XXXX XXXX XXXX XXXX, начиная с start и до stop включительно.
    """
    for number in range(start, stop + 1):
        card_number = f"{number:016d}"
        formatted = " ".join(card_number[i : i + 4] for i in range(0, 16, 4))
        yield formatted
