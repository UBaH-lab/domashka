
from src.processing import sort_by_date, filter_by_state
import sys
import os
import pytest

# Добавляем путь до папки src
sys.path.insert(0, os.path.abspath(r"C:\Users\Ivan\PycharmProjects\PythonProject19\src"))


@pytest.fixture
def transactions():
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'},
        {'id': 2, 'state': 'PENDING', 'date': '2020-01-02T12:00:00'},
        {'id': 3, 'state': 'CANCELED', 'date': '2019-12-31T23:59:59'},
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ('EXECUTED', [1]),
        ('CANCELED', [3]),
        ('NONE', []),
        (None, [1, 2, 3]),
    ]
)
def test_filter_by_state(transactions, state, expected_ids):
    filtered = filter_by_state(transactions, state)
    filtered_ids = [t['id'] for t in filtered]
    assert filtered_ids == expected_ids


@pytest.mark.parametrize(
    "ascending, expected_order",
    [
        (True, ['2019-12-31T23:59:59', '2020-01-01T10:00:00', '2020-01-02T12:00:00']),
        (False, ['2020-01-02T12:00:00', '2020-01-01T10:00:00', '2019-12-31T23:59:59']),
    ]
)
def test_sort_by_date(transactions, ascending, expected_order):
    sorted_list = sort_by_date(transactions, ascending=ascending)
    dates = [t['date'] for t in sorted_list]
    assert dates == expected_order


if __name__ == "__main__":
    import pytest
    pytest.main([os.path.abspath(__file__)])
