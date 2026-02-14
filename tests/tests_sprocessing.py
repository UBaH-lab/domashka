
import sys
import os

# Добавляем путь до папки src
sys.path.insert(0, os.path.abspath(r"C:\Users\Ivan\PycharmProjects\PythonProject19\src"))

from processing import sort_by_date, filter_by_state


# Тестовые данные
transactions = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'},
    {'id': 2, 'state': 'PENDING', 'date': '2020-01-02T12:00:00'},
    {'id': 3, 'state': 'CANCELED', 'date': '2019-12-31T23:59:59'},
]

def test_filter_by_state():
    # Проверка фильтрации по состоянию
    assert [t['id'] for t in filter_by_state(transactions, 'EXECUTED')] == [1]
    assert [t['id'] for t in filter_by_state(transactions, 'CANCELED')] == [3]
    # Если статус не найден — список пуст
    assert filter_by_state(transactions, 'NONE') == []
    # Без указания статуса — возвращает все
    assert filter_by_state(transactions, None) == transactions

def test_sort_by_date():
    # Проверка сортировки по дате
    sorted_list = sort_by_date(transactions)
    dates = [t['date'] for t in sorted_list]
    assert dates == sorted(dates)  # по возрастанию
    # По убыванию
    sorted_list_desc = sort_by_date(transactions, ascending=False)
    dates_desc = [t['date'] for t in sorted_list_desc]
    assert dates_desc == sorted(dates, reverse=True)
