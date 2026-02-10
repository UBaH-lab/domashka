import pytest

transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

def test_filter_by_state():
    # Проверка фильтрации по 'EXECUTED'
    result_exec = filter_by_state(transactions, 'EXECUTED')
    assert [trans['id'] for trans in result_exec] == [41428829, 939719570]

    # Проверка фильтрации по 'CANCELED'
    result_canceled = filter_by_state(transactions, 'CANCELED')
    assert [trans['id'] for trans in result_canceled] == [594226727, 615064591]

    # Проверка возврата всех транзакций, если state=None
    all_transactions = filter_by_state(transactions)
    assert len(all_transactions) == len(transactions)

    # Проверка с несуществующим статусом возвращает пустой список
    empty_result = filter_by_state(transactions, 'NONEXISTENT')
    assert empty_result == []

def test_sort_by_date():
    # Проверка сортировки по возрастанию
    sorted_asc = sort_by_date(transactions, ascending=True)
    dates_asc = [t['date'] for t in sorted_asc]
    assert dates_asc == sorted(dates_asc)

    # Проверка сортировки по убыванию
    sorted_desc = sort_by_date(transactions, ascending=False)
    dates_desc = [t['date'] for t in sorted_desc]
    assert dates_desc == sorted(dates_desc, reverse=True)

    # Проверка с одинаковыми датами
    duplicate_data = [
        {'id': 1, 'date': '2020-01-01T00:00:00'},
        {'id': 2, 'date': '2020-01-01T00:00:00'},
        {'id': 3, 'date': '2019-12-31T23:59:59'}
    ]
    sorted_dup = sort_by_date(duplicate_data, ascending=True)
    assert [t['date'] for t in sorted_dup] == ['2019-12-31T23:59:59', '2020-01-01T00:00:00', '2020-01-01T00:00:00']

    # Проверка с неверным форматом даты
    invalid_data = [
        {'id': 1, 'date': '2020-01-01T00:00:00'},
        {'id': 2, 'date': 'invalid-date'},
    ]
    with pytest.raises(ValueError):
        sort_by_date(invalid_data, ascending=True)

# Запуск тестов через pytest, если запустите этот скрипт напрямую
if __name__ == "__main__":
    pytest.main([__file__])