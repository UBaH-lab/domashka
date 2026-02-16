def sort_by_date(transactions, ascending=True) -> str:
    """
    Сортирует список транзакций по дате.
    По умолчанию сортировка по возрастанию.
    """
    return sorted(transactions, key=lambda transaction: transaction["date"], reverse=not ascending)


def filter_by_state(transactions, state=None) -> str:
    """
    Фильтрует транзакции по состоянию.
    Если 'state' не передаёт все транзакции.
    """
    if state is None:
        return transactions
    filtered_transactions = []
    for transaction in transactions:
        if transaction['state'] == state:
            filtered_transactions.append(transaction)
    return filtered_transactions


transactions = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

sorted_transactions_date = sort_by_date(transactions)
print(sorted_transactions_date)
filter_by_state(transactions)
