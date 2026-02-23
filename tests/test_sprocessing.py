import pytest


from src.processing import sort_by_date, filter_by_state

# Фикстура
# transactions
# Что делает:
# - обеспечивает набор тестовых транзакций, который используется во всех тестах ниже.
# - каждый элемент содержит id, state и date (ISO-строка).
# - данный набор позволяет проверять фильтрацию по состоянию и сортировку по дате.


@pytest.fixture
def transactions():
    """
    Набор тестовых транзакций:
    - id: уникальный идентификатор транзакции
    - state: одно из EXECUTED, PENDING, CANCELED
    - date: дата и время в ISO-формате
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "2020-01-01T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2020-01-02T12:00:00"},
        {"id": 3, "state": "CANCELED", "date": "2019-12-31T23:59:59"},
    ]


# Параметризация для фильтрации по состоянию
# Что делает:
# - перечисляет набор кейсов, где each case имеет:
#   - state: состояние, по которому фильтруем (или None для отключения фильтра)
#   - expected_ids: ожидаемые id после фильтрации
#   - description: краткое описание кейса (для удобного именования тестов
cases_state = [
    {"state": "EXECUTED", "expected_ids": [1], "description": "only_executed"},
    {"state": "CANCELED", "expected_ids": [3], "description": "only_canceled"},
    {"state": "NONE", "expected_ids": [], "description": "unknown_state"},
    {"state": None, "expected_ids": [1, 2, 3], "description": "no_state_filter"},
]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1]),
        ("CANCELED", [3]),
        ("NONE", []),
        (None, [1, 2, 3]),
    ],
)
def test_filter_by_state(transactions, state, expected_ids):
    """
    Тестирует функцию filter_by_state из src.processing.
    - Для конкретного state возвращает только те транзакции, у которых совпадает state.
    - Если state None — возвращаются все транзакции (без фильтрации).
    - Для неизвестного состояния возвращается пустой список.
    """
    filtered = filter_by_state(transactions, state)
    filtered_ids = [t["id"] for t in filtered]
    assert filtered_ids == expected_ids


# Параметризация для сортировки по дате
# Что делает:
# - описывает два кейса сортировки: по возрастанию и по убыванию.
# - каждый кейс содержит:
#   - ascending: направление сортировки (True/False)
#   - expected_order: ожидаемый порядок дат в виде списка строк
#   - description: краткое описание кейса
cases_order = [
    {
        "ascending": True,
        "expected_order": [
            "2019-12-31T23:59:59",
            "2020-01-01T10:00:00",
            "2020-01-02T12:00:00",
        ],
        "description": "ascending",
    },
    {
        "ascending": False,
        "expected_order": [
            "2020-01-02T12:00:00",
            "2020-01-01T10:00:00",
            "2019-12-31T23:59:59",
        ],
        "description": "descending",
    },
]


@pytest.mark.parametrize(
    "ascending, expected_order",
    [
        (True, ["2019-12-31T23:59:59", "2020-01-01T10:00:00", "2020-01-02T12:00:00"]),
        (False, ["2020-01-02T12:00:00", "2020-01-01T10:00:00", "2019-12-31T23:59:59"]),
    ],
)
def test_sort_by_date(transactions, ascending, expected_order):
    """
    Тестирует sort_by_date из src.processing.
    - Проверяем корректную сортировку по полю date в заданном направлении.
    - Ожидаем, что итоговый упорядоченный список возвращает даты в нужном порядке.
    """
    sorted_list = sort_by_date(transactions, ascending=ascending)
    dates = [t["date"] for t in sorted_list]
    assert dates == expected_order


if __name__ == "__main__":
    pytest.main([__file__])
