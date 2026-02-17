from typing import List, Dict, Optional

def sort_by_date(transactions: List[Dict], ascending: bool = True) -> List[Dict]:
    """
    Сортирует список транзакций по дате.
    По умолчанию сортировка по возрастанию.
    """
    return sorted(transactions, key=lambda transaction: transaction["date"], reverse=not ascending)

def filter_by_state(transactions: List[Dict], state: Optional[str] = None) -> List[Dict]:
    """
    Фильтрует транзакции по состоянию.
    Если 'state' не передаётся, возвращает все транзакции.
    """
    if state is None:
        return transactions
    filtered_transactions = []
    for transaction in transactions:
        if transaction['state'] == state:
            filtered_transactions.append(transaction)
    return filtered_transactions