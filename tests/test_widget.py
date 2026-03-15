import pytest

from src.widget import get_date, mask_account_card

# Фикстуры
# Эти фикстуры предназначены для передачи значений в тесты через параметризацию
# и позволяют явно описать, что именно подаётся на вход тестируемым функциям.


@pytest.fixture
def input_str_mask(request):
    """Возвращает строку-исходник для маскировки карт/счётов.

    Значение приходит через request.param благодаря indirect-переменной в тестах.
    Примеры входных данных приводятся в тестовой парадигме ниже.
    """
    return request.param


@pytest.fixture
def input_str_date_valid(request):
    """Возвращает валидную ISO-строку даты/времени для теста get_date.

    Значение приходит через request.param благодаря indirect-переменной в тестах.
    """
    return request.param


@pytest.fixture
def input_str_date_err(request):
    """Возвращает некорректную строку даты для теста ошибок get_date.

    Значение приходит через request.param благодаря indirect-переменной в тестах.
    """
    return request.param


# Тесты
# 1) Тест маскировки: проверяем разные входные строки и соответствующие ожидаемые результаты.
@pytest.mark.parametrize(
    "input_str_mask, expected_output",
    [
        ("Visa Gold 5999414228426353", "Visa Gold **** ****6353"),
        (
            "Mastercard Platinum 1234 5678 9876 5432",
            "Mastercard Platinum **** ****5432",
        ),
        ("Мастеркард 1111222233334444", "Мастеркард **** ****4444"),
        ("Счет 1234567890123456", "Счет **3456"),
        ("Счет 9876543210", "Счет **!"),
        ("Счет 123", "Счет **!"),
        ("Нет данных", "Нет данных"),
        ("", ""),
    ],
    indirect=["input_str_mask"],  # передаём входную строку в фикстуру input_str_mask
)
def test_mask_account_card(input_str_mask, expected_output):
    """Проверка функций маскировки mask_account_card.

    - input_str_mask: строка-источник для маскировки (через фикстуру, параметризована через indirect).
    - expected_output: ожидаемая строка после маскировки.
    - coverage: карты, счета и пустые/некорректные данные.
    - Примечание: некоторые ожидаемые значения могут выглядеть необычно (например, "Счет 9876543210" -> "Счет **!").
      Это отражает текущую логику тестируемой функции; при необходимости можно скорректировать тестовую выборку.
    """
    assert mask_account_card(input_str_mask) == expected_output


# 2) Тест дат: проверяем корректность преобразования ISO-строк к DD.MM.YYYY.
@pytest.mark.parametrize(
    "input_str_date_valid, expected_output",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
        ("2022-12-31T23:59:59", "31.12.2022"),
        ("2024-07-15", "15.07.2024"),
    ],
    indirect=["input_str_date_valid"],
)
def test_get_date_valid(input_str_date_valid, expected_output):
    """Проверка функции get_date: преобразование ISO-строки в формат DD.MM.YYYY.

    - input_str_date_valid передаётся через фикстуру (indirect).
    - expected_output — ожидаемая строка в формате DD.MM.YYYY.
    """
    assert get_date(input_str_date_valid) == expected_output


# 3) Тест ошибок дат: проверяем, что неверные входы вызывают ValueError.
@pytest.mark.parametrize(
    "input_str_date_err, expected_exception",
    [
        ("2024-13-01T00:00:00", ValueError),  # несуществующий месяц
        ("2024-02-30T00:00:00", ValueError),  # несуществующий день
        ("Некорректная строка", ValueError),  # неверный формат
        ("", ValueError),  # пустая строка
    ],
    indirect=["input_str_date_err"],
)
def test_get_date_errors(input_str_date_err, expected_exception):
    """Проверка того, что неверный ввод в get_date вызывает исключение ValueError."""
    with pytest.raises(expected_exception):
        get_date(input_str_date_err)
