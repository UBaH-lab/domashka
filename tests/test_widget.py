import pytest
from src.widget import mask_account_card, get_date


# Фикстура для подготовки входной строки для тестов mask_account_card
@pytest.fixture
def input_str_mask(request):  # Получаем текущий параметр из request.param

    return request.param  # Пока просто возвращаем без изменений


# Фикстура для подготовки корректной даты для тестов get_date (валидных)
@pytest.fixture
def input_str_date_valid(request):
    # Можно добавить валидацию или предобработку даты
    return request.param


# Фикстура для подготовки "ошибочных" дат для тестов get_date (ошибки)
@pytest.fixture
def input_str_date_err(request):
    # Также можно подготовить или привести данные к строке
    return request.param


# Тестирование mask_account_card с параметризацией и фикстурой
@pytest.mark.parametrize(
    # Указываем, что параметр input_str_mask передается через фикстуру input_str_mask
    "input_str_mask, expected_output",
    [
        ("Visa Gold 5999414228426353", "Visa Gold **** ****6353"),
        ("Mastercard Platinum 1234 5678 9876 5432", "Mastercard Platinum **** ****5432"),
        ("Мастеркард 1111222233334444", "Мастеркард **** ****4444"),
        ("Счет 1234567890123456", "Счет **3456"),
        ("Счет 9876543210", "Счет **!"),
        ("Счет 123", "Счет **!"),
        ("Нет данных", "Нет данных"),
        ("", ""),
    ],
    indirect=["input_str_mask"]  # передаем input_str_mask через одноименную фикстуру
)
def test_mask_account_card(input_str_mask, expected_output):
    # Проверяем, что маскирование номера карты работает корректно
    assert mask_account_card(input_str_mask) == expected_output


# Тестирование get_date с корректными датами через фикстуру
@pytest.mark.parametrize(
    "input_str_date_valid, expected_output",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
        ("2022-12-31T23:59:59", "31.12.2022"),
        ("2024-07-15", "15.07.2024"),
    ],
    indirect=["input_str_date_valid"]  # передаем через фикстуру
)
def test_get_date_valid(input_str_date_valid, expected_output):
    # Проверяем корректное форматирование даты
    assert get_date(input_str_date_valid) == expected_output


# Тестирование get_date на ошибки, ожидаем исключение
@pytest.mark.parametrize(
    "input_str_date_err, expected_exception",
    [
        ("2024-13-01T00:00:00", ValueError),  # несуществующий месяц
        ("2024-02-30T00:00:00", ValueError),  # несуществующий день
        ("Некорректная строка", ValueError),    # неверный формат
        ("", ValueError),                        # пустая строка
    ],
    indirect=["input_str_date_err"]  # через фикстуру
)
def test_get_date_errors(input_str_date_err, expected_exception):
    # Проверяем, что при ошибочном вводе выбрасывается ожидаемое исключение
    with pytest.raises(expected_exception):
        get_date(input_str_date_err)
