"""
Модуль generators содержит генераторы для работы с транзакциями.

Генераторы — это специальный тип функций, которые возвращают значения
по одному с помощью ключевого слова yield, а не все сразу.

Преимущества генераторов:
- Экономия памяти (не хранят весь список в памяти)
- Ленивые вычисления (вычисляют только когда нужно)
- Возможность работать с бесконечными последовательностями
"""

from typing import Dict, Generator, List


def filter_by_currency(
    transactions: List[Dict], currency_code: str
) -> Generator[Dict, None, None]:
    """
    Фильтрует транзакции по коду валюты.

    Проходит по списку транзакций и возвращает только те,
    у которых валюта совпадает с указанным кодом.

    Args:
        transactions (List[Dict]): Список словарей с транзакциями.
            Каждая транзакция должна иметь структуру:
            {
                "operationAmount": {
                    "currency": {
                        "code": "USD"  # или "RUB", "EUR" и т.д.
                    }
                }
            }
        currency_code (str): Код валюты для фильтрации
            (например, "USD", "RUB").

    Yields:
        Dict: Транзакции, у которых валюта совпадает с currency_code.

    Examples:
        >>> transactions = [
        ...     {"operationAmount": {"currency": {"code": "USD"}}},
        ...     {"operationAmount": {"currency": {"code": "RUB"}}},
        ...     {"operationAmount": {"currency": {"code": "USD"}}},
        ... ]
        >>> usd_txns = list(
        ...     filter_by_currency(transactions, "USD")
        ... )
        >>> len(usd_txns)
        2

    Note:
        Генератор возвращает значения по одному, что экономит память
        при работе с большими списками транзакций.
    """
    for transaction in transactions:
        currency = transaction["operationAmount"]["currency"]["code"]
        if currency == currency_code:
            yield transaction


def transaction_descriptions(
    transactions: List[Dict],
) -> Generator[str, None, None]:
    """
    Извлекает описания из транзакций.

    Генератор проходит по списку транзакций и возвращает
    описание каждой.

    Args:
        transactions (List[Dict]): Список словарей с транзакциями.
            Ожидается наличие ключа "description" в каждой транзакции.

    Yields:
        str: Описание текущей транзакции.
            Если описание отсутствует, возвращает пустую строку.

    Examples:
        >>> transactions = [
        ...     {"description": "Оплата интернета"},
        ...     {"description": "Перевод другу"},
        ... ]
        >>> descs = list(transaction_descriptions(transactions))
        >>> descs
        ['Оплата интернета', 'Перевод другу']

    Note:
        Использует .get() со значением по умолчанию "",
        чтобы избежать KeyError при отсутствии описания.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(
    start: int = 1, stop: int = 9999999999999999
) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.

    Создает последовательность номеров карт от start до stop включительно,
    форматируя их в стандартный вид с пробелами каждые 4 цифры.

    Args:
        start (int): Начальный номер карты (по умолчанию 1).
        stop (int): Конечный номер карты включительно
            (по умолчанию 9999999999999999 — максимальный 16-значный).

    Yields:
        str: Номер карты в формате "XXXX XXXX XXXX XXXX".

    Examples:
        >>> gen = card_number_generator(1, 3)
        >>> list(gen)
        ['0000 0000 0000 0001', '0000 0000 0000 0002',
         '0000 0000 0000 0003']

        >>> gen = card_number_generator(
        ...     1234567890123456, 1234567890123456
        ... )
        >>> next(gen)
        '1234 5678 9012 3456'

    Note:
        - Номера дополняются нулями слева до 16 цифр
        - Формат удобен для отображения пользователю
        - Генератор может создавать очень длинные последовательности
          без загрузки их в память целиком
    """
    for number in range(start, stop + 1):
        card_number = f"{number:016d}"  # Дополняем нулями до 16 цифр
        formatted = " ".join(card_number[i : i + 4] for i in range(0, 16, 4))
        yield formatted
