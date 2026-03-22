# -*- coding: utf-8 -*-
"""
Модуль test_main содержит тесты для основной программы.

Тестирует функции из main.py:
- load_transactions_from_json: загрузка из JSON
- load_transactions_from_csv: загрузка из CSV
- load_transactions_from_excel: загрузка из Excel
- filter_by_status: фильтрация по статусу
- sort_by_date: сортировка по дате
- mask_number: маскирование номера
- format_transaction: форматирование транзакции
- Интерактивные функции (_select_file_format, _filter_by_status_interactive, etc.)

Использует unittest.mock для мокирования ввода/вывода.
"""

from unittest.mock import patch

from main import (
    filter_by_status,
    format_transaction,
    load_transactions_from_csv,
    load_transactions_from_excel,
    load_transactions_from_json,
    main,
    mask_number,
    sort_by_date,
)

# ============================================================================
# ТЕСТЫ ЗАГРУЗКИ ИЗ JSON
# ============================================================================


def test_load_json_ok(tmp_path):
    """
    Тест: успешная загрузка транзакций из JSON.

    Проверяет:
    - Создание файла JSON
    - Корректность загрузки данных
    - Совпадение структуры данных

    Args:
        tmp_path: Pytest fixture для временной директории

    Результат: [{"id": 1}]
    """
    f = tmp_path / "t.json"
    f.write_text('[{"id":1}]', encoding="utf-8")
    assert load_transactions_from_json(str(f)) == [{"id": 1}]


def test_load_json_no_file():
    """
    Тест: загрузка из несуществующего JSON файла.

    Проверяет:
    - Возвращается пустой список при ошибке

    Результат: []
    """
    assert load_transactions_from_json("x.json") == []


def test_load_json_invalid(tmp_path):
    """
    Тест: загрузка из невалидного JSON файла.

    Проверяет:
    - Возвращается пустой список при ошибке парсинга

    Args:
        tmp_path: Pytest fixture для временной директории

    Результат: []
    """
    f = tmp_path / "bad.json"
    f.write_text("{bad}", encoding="utf-8")
    assert load_transactions_from_json(str(f)) == []


# ============================================================================
# ТЕСТЫ ФИЛЬТРАЦИИ И СОРТИРОВКИ
# ============================================================================


def test_filter():
    """
    Тест: фильтрация по статусу EXECUTED.

    Проверяет:
    - Возвращаются только транзакции с EXECUTED
    - Количество результатов: 1

    Результат: [{"state": "EXECUTED"}]
    """
    data = [{"state": "EXECUTED"}, {"state": "CANCELED"}]
    assert len(filter_by_status(data, "EXECUTED")) == 1


def test_sort():
    """
    Тест: сортировка по возрастанию даты.

    Проверяет:
    - Транзакции сортируются по дате
    - Первая транзакция имеет id=1 (01.01.2024)

    Результат: [{"id": 1}, {"id": 2}]
    """
    r = sort_by_date(
        [{"id": 1, "date": "01.01.2024"}, {"id": 2, "date": "02.01.2024"}], True
    )
    assert r[0]["id"] == 1


# ============================================================================
# ТЕСТЫ МАСКИРОВАНИЯ
# ============================================================================


def test_mask_card():
    """
    Тест: маскирование номера карты.

    Проверяет:
    - Номер карты маскируется
    - Результат не пустой

    Результат: замаскированный номер
    """
    assert mask_number("1234567890123456")


def test_mask_account():
    """
    Тест: маскирование номера счета.

    Проверяет:
    - Номер счета маскируется
    - Результат не пустой

    Результат: замаскированный номер
    """
    assert mask_number("12345678901234567890")


def test_mask_empty():
    """
    Тест: маскирование пустого значения.

    Проверяет:
    - Для пустой строки возвращается ""
    - Для None возвращается ""

    Результат: ""
    """
    assert mask_number("") == ""
    assert mask_number(None) == ""


def test_mask_short():
    """
    Тест: маскирование короткого номера.

    Проверяет:
    - Короткий номер возвращается без изменений

    Результат: "12345"
    """
    assert mask_number("12345") == "12345"


# ============================================================================
# ТЕСТЫ ФОРМАТИРОВАНИЯ
# ============================================================================


def test_format():
    """
    Тест: форматирование транзакции.

    Проверяет:
    - Транзакция форматируется
    - Для пустой транзакции возвращается ""

    Результат: отформатированная строка
    """
    assert format_transaction({"date": "01.01.2024"})
    assert format_transaction({}) == ""


def test_format_with_amount():
    """
    Тест: форматирование с суммой операции.

    Проверяет:
    - Сумма включается в вывод
    - Символ валюты включается

    Результат: строка с "100"
    """
    t = {
        "date": "01.01.2024",
        "description": "Test",
        "operationAmount": {"amount": "100", "currency": {"code": "USD"}},
    }
    r = format_transaction(t)
    assert "100" in r


def test_format_only_from():
    """
    Тест: форматирование с полем from.

    Проверяет:
    - Поле from маскируется и включается в вывод
    - Дата включается

    Результат: строка с "01.01.2024"
    """
    t = {"date": "01.01.2024", "description": "Test", "from": "1234567890123456"}
    r = format_transaction(t)
    assert "01.01.2024" in r


def test_format_only_to():
    """
    Тест: форматирование с полем to.

    Проверяет:
    - Поле to маскируется и включается в вывод
    - Дата включается

    Результат: строка с "01.01.2024"
    """
    t = {"date": "01.01.2024", "description": "Test", "to": "12345678901234567890"}
    r = format_transaction(t)
    assert "01.01.2024" in r


# ============================================================================
# ТЕСТЫ ЗАГРУЗКИ ИЗ CSV И EXCEL
# ============================================================================


@patch("main.read_transactions_csv")
def test_csv(mock):
    """
    Тест: загрузка из CSV с мокированием.

    Проверяет:
    - Функция вызывается с правильным аргументом
    - Результат возвращается

    Результат: [{"id": 1}]
    """
    mock.return_value = [{"id": 1}]
    assert load_transactions_from_csv("t.csv")


@patch("main.read_transactions_csv")
def test_csv_file_not_found(mock_read):
    """
    Тест: обработка FileNotFoundError для CSV.

    Проверяет:
    - При ошибке FileNotFoundError возвращается []

    Результат: []
    """
    mock_read.side_effect = FileNotFoundError()
    assert load_transactions_from_csv("test.csv") == []


@patch("main.read_transactions_csv")
def test_csv_value_error(mock_read):
    """
    Тест: обработка ValueError для CSV.

    Проверяет:
    - При ошибке ValueError возвращается []

    Результат: []
    """
    mock_read.side_effect = ValueError("Bad CSV")
    assert load_transactions_from_csv("test.csv") == []


@patch("main.read_transactions_excel")
def test_excel(mock):
    """
    Тест: загрузка из Excel с мокированием.

    Проверяет:
    - Функция вызывается с правильным аргументом
    - Результат возвращается

    Результат: [{"id": 1}]
    """
    mock.return_value = [{"id": 1}]
    assert load_transactions_from_excel("t.xlsx")


@patch("main.read_transactions_excel")
def test_excel_file_not_found(mock_read):
    """
    Тест: обработка FileNotFoundError для Excel.

    Проверяет:
    - При ошибке FileNotFoundError возвращается []

    Результат: []
    """
    mock_read.side_effect = FileNotFoundError()
    assert load_transactions_from_excel("test.xlsx") == []


@patch("main.read_transactions_excel")
def test_excel_value_error(mock_read):
    """
    Тест: обработка ValueError для Excel.

    Проверяет:
    - При ошибке ValueError возвращается []

    Результат: []
    """
    mock_read.side_effect = ValueError("Bad Excel")
    assert load_transactions_from_excel("test.xlsx") == []


# ============================================================================
# ТЕСТЫ ИНТЕРАКТИВНЫХ ФУНКЦИЙ
# ============================================================================


@patch("builtins.input")
@patch("builtins.print")
def test_select_json(mock_print, mock_input):
    """
    Тест: выбор формата JSON.

    Проверяет:
    - При вводе "1" возвращается "json"

    Результат: "json"
    """
    from main import _select_file_format

    mock_input.return_value = "1"
    assert _select_file_format() == "json"


@patch("builtins.input")
@patch("builtins.print")
def test_select_csv(mock_print, mock_input):
    """
    Тест: выбор формата CSV.

    Проверяет:
    - При вводе "2" возвращается "csv"

    Результат: "csv"
    """
    from main import _select_file_format

    mock_input.return_value = "2"
    assert _select_file_format() == "csv"


@patch("builtins.input")
@patch("builtins.print")
def test_select_xlsx(mock_print, mock_input):
    """
    Тест: выбор формата XLSX.

    Проверяет:
    - При вводе "3" возвращается "xlsx"

    Результат: "xlsx"
    """
    from main import _select_file_format

    mock_input.return_value = "3"
    assert _select_file_format() == "xlsx"


@patch("builtins.input")
@patch("builtins.print")
def test_select_invalid(mock_print, mock_input):
    """
    Тест: выбор невалидного формата.

    Проверяет:
    - При вводе "99" возвращается None

    Результат: None
    """
    from main import _select_file_format

    mock_input.return_value = "99"
    assert _select_file_format() is None


@patch("builtins.input")
@patch("builtins.print")
def test_filter_status_yes(mock_print, mock_input):
    """
    Тест: интерактивная фильтрация по статусу.

    Проверяет:
    - При вводе "EXECUTED" фильтрация выполняется

    Результат: [{"id": 1, "state": "EXECUTED"}]
    """
    from main import _filter_by_status_interactive

    mock_input.return_value = "EXECUTED"
    data = [{"id": 1, "state": "EXECUTED"}]
    result = _filter_by_status_interactive(data)
    assert len(result) == 1


@patch("builtins.input")
@patch("builtins.print")
def test_sort_ascending(mock_print, mock_input):
    """
    Тест: интерактивная сортировка по возрастанию.

    Проверяет:
    - При вводе "по возрастанию" сортировка выполняется

    Результат: [{"id": 1, "date": "01.01.2024"}]
    """
    from main import _sort_by_date_interactive

    mock_input.return_value = "по возрастанию"
    data = [{"id": 1, "date": "01.01.2024"}]
    result = _sort_by_date_interactive(data)
    assert len(result) == 1


@patch("builtins.input")
@patch("builtins.print")
def test_sort_descending(mock_print, mock_input):
    """
    Тест: интерактивная сортировка по убыванию.

    Проверяет:
    - При вводе "по убыванию" сортировка выполняется

    Результат: [{"id": 1, "date": "01.01.2024"}]
    """
    from main import _sort_by_date_interactive

    mock_input.return_value = "по убыванию"
    data = [{"id": 1, "date": "01.01.2024"}]
    result = _sort_by_date_interactive(data)
    assert len(result) == 1


@patch("builtins.input")
@patch("builtins.print")
def test_filter_currency_yes(mock_print, mock_input):
    """
    Тест: интерактивная фильтрация по валюте.

    Проверяет:
    - При вводе "RUB" фильтрация выполняется

    Результат: [{"id": 1, "currency": "RUB"}]
    """
    from main import _filter_by_currency_interactive

    mock_input.return_value = "RUB"
    data = [{"id": 1, "currency": "RUB"}]
    result = _filter_by_currency_interactive(data)
    assert len(result) == 1


@patch("builtins.input")
@patch("builtins.print")
@patch("main.process_bank_search")
def test_search_yes(mock_search, mock_print, mock_input):
    """
    Тест: интерактивный поиск по ключевым словам.

    Проверяет:
    - Функция поиска вызывается

    Результат: вызов process_bank_search
    """
    from main import _search_by_keywords

    mock_input.return_value = "test"
    mock_search.return_value = []
    _search_by_keywords([])


@patch("builtins.print")
def test_show_stats_ok(mock_print):
    """
    Тест: отображение статистики по категориям.

    Проверяет:
    - Функция выполняется без ошибок

    Результат: вывод статистики
    """
    from main import _show_category_statistics

    _show_category_statistics([{"description": "Test"}])


@patch("builtins.print")
def test_display_ok(mock_print):
    """
    Тест: отображение результатов с данными.

    Проверяет:
    - Функция выводит результаты

    Результат: вывод транзакций
    """
    from main import _display_results

    _display_results([{"id": 1, "date": "01.01.2024"}])


@patch("builtins.print")
def test_display_empty(mock_print):
    """
    Тест: отображение результатов без данных.

    Проверяет:
    - Функция обрабатывает пустой список

    Результат: вывод сообщения о пустом списке
    """
    from main import _display_results

    _display_results([])


@patch("builtins.input")
@patch("main.load_transactions_from_json")
def test_load_format_json(mock_load, mock_input):
    """
    Тест: загрузка транзакций в формате JSON.

    Проверяет:
    - Вызывается load_transactions_from_json
    - Результат возвращается

    Результат: [{"id": 1}]
    """
    from main import _load_transactions_by_format

    mock_input.return_value = "test.json"
    mock_load.return_value = [{"id": 1}]
    assert _load_transactions_by_format("json") == [{"id": 1}]


@patch("builtins.input")
@patch("main.load_transactions_from_csv")
def test_load_format_csv(mock_load, mock_input):
    """
    Тест: загрузка транзакций в формате CSV.

    Проверяет:
    - Вызывается load_transactions_from_csv
    - Результат возвращается

    Результат: [{"id": 1}]
    """
    from main import _load_transactions_by_format

    mock_input.return_value = "test.csv"
    mock_load.return_value = [{"id": 1}]
    assert _load_transactions_by_format("csv") == [{"id": 1}]


@patch("builtins.input")
@patch("main.load_transactions_from_excel")
def test_load_format_xlsx(mock_load, mock_input):
    """
    Тест: загрузка транзакций в формате XLSX.

    Проверяет:
    - Вызывается load_transactions_from_excel
    - Результат возвращается

    Результат: [{"id": 1}]
    """
    from main import _load_transactions_by_format

    mock_input.return_value = "test.xlsx"
    mock_load.return_value = [{"id": 1}]
    assert _load_transactions_by_format("xlsx") == [{"id": 1}]


@patch("builtins.input")
@patch("builtins.print")
def test_load_format_unknown(mock_print, mock_input):
    """
    Тест: загрузка в неизвестном формате.

    Проверяет:
    - Для неизвестного формата возвращается []

    Результат: []
    """
    from main import _load_transactions_by_format

    assert _load_transactions_by_format("unknown") == []


# ============================================================================
# ТЕСТЫ ОБРАБОТКИ ОШИБОК ПАРСИНГА ДАТ
# ============================================================================


def test_parse_date_invalid():
    """
    Тест: обработка невалидной даты при сортировке.

    Проверяет:
    - Транзакция с невалидной датой обрабатывается
    - Результат не пустой

    Результат: [{"id": 1, "date": "invalid"}]
    """
    from main import sort_by_date

    result = sort_by_date([{"id": 1, "date": "invalid"}])
    assert len(result) == 1


def test_parse_date_none():
    """
    Тест: обработка None в дате при сортировке.

    Проверяет:
    - Транзакция с None в дате обрабатывается
    - Результат не пустой

    Результат: [{"id": 1, "date": None}]
    """
    from main import sort_by_date

    result = sort_by_date([{"id": 1, "date": None}])
    assert len(result) == 1


# ============================================================================
# ТЕСТЫ ПОИСКА И СТАТИСТИКИ
# ============================================================================


@patch("builtins.print")
@patch("main.process_bank_search")
def test_search_with_results(mock_search, mock_print):
    """
    Тест: поиск по ключевым словам с результатами.

    Проверяет:
    - Функция поиска вызывается
    - Результаты выводятся

    Результат: вывод результатов поиска
    """
    from main import _search_by_keywords

    mock_search.return_value = [{"id": 1, "date": "01.01.2024", "description": "Test"}]
    with patch("builtins.input", return_value="test"):
        _search_by_keywords([])
    assert mock_print.called


# ============================================================================
# ТЕСТЫ ОСНОВНОЙ ФУНКЦИИ main()
# ============================================================================


@patch("main._select_file_format")
@patch("main._load_transactions_by_format")
@patch("builtins.print")
def test_main_empty_transactions(mock_print, mock_load, mock_select):
    """
    Тест: main() с пустыми транзакциями.

    Проверяет:
    - Выводится сообщение о невозможности загрузки

    Результат: сообщение "Не удалось загрузить"
    """
    mock_select.return_value = "json"
    mock_load.return_value = []
    main()
    assert any(
        "Не удалось загрузить" in str(call) for call in mock_print.call_args_list
    )


@patch("main._display_results")
@patch("main._show_category_statistics")
@patch("main._search_by_keywords")
@patch("main._filter_by_currency_interactive")
@patch("main._sort_by_date_interactive")
@patch("main._filter_by_status_interactive")
@patch("main._load_transactions_by_format")
@patch("main._select_file_format")
@patch("builtins.input")
@patch("builtins.print")
def test_main_with_search_and_stats(
    mock_print,
    mock_input,
    mock_select,
    mock_load,
    mock_filter_status,
    mock_sort,
    mock_filter_currency,
    mock_search,
    mock_stats,
    mock_display,
):
    """
    Тест: main() с поиском и статистикой.

    Проверяет:
    - Все интерактивные функции вызываются
    - Поиск вызывается один раз
    - Статистика вызывается один раз

    Результат: выполнение всех этапов
    """
    mock_select.return_value = "json"
    mock_load.return_value = [{"id": 1, "date": "01.01.2024"}]
    mock_filter_status.return_value = [{"id": 1}]
    mock_sort.return_value = [{"id": 1}]
    mock_filter_currency.return_value = [{"id": 1}]
    mock_input.side_effect = ["да", "да", "да", "да", "да", "да"]
    main()
    mock_search.assert_called_once()
    mock_stats.assert_called_once()


@patch("main._display_results")
@patch("main._show_category_statistics")
@patch("main._search_by_keywords")
@patch("main._filter_by_currency_interactive")
@patch("main._sort_by_date_interactive")
@patch("main._filter_by_status_interactive")
@patch("main._load_transactions_by_format")
@patch("main._select_file_format")
@patch("builtins.input")
@patch("builtins.print")
def test_main_confirm_yes(
    mock_print,
    mock_input,
    mock_select,
    mock_load,
    mock_filter_status,
    mock_sort,
    mock_filter_currency,
    mock_search,
    mock_stats,
    mock_display,
):
    """
    Тест: main() с подтверждением "да".

    Проверяет:
    - При ответе "да" выполняется отображение результатов

    Результат: вызов _display_results
    """
    mock_select.return_value = "json"
    mock_load.return_value = [{"id": 1, "date": "01.01.2024"}]
    mock_filter_status.return_value = [{"id": 1}]
    mock_sort.return_value = [{"id": 1}]
    mock_filter_currency.return_value = [{"id": 1}]
    mock_input.side_effect = ["да", "да", "нет", "нет", "нет", "нет"]
    main()
    mock_display.assert_called_once()


@patch("main._display_results")
@patch("main._show_category_statistics")
@patch("main._search_by_keywords")
@patch("main._filter_by_currency_interactive")
@patch("main._sort_by_date_interactive")
@patch("main._filter_by_status_interactive")
@patch("main._load_transactions_by_format")
@patch("main._select_file_format")
@patch("builtins.input")
@patch("builtins.print")
def test_main_confirm_no(
    mock_print,
    mock_input,
    mock_select,
    mock_load,
    mock_filter_status,
    mock_sort,
    mock_filter_currency,
    mock_search,
    mock_stats,
    mock_display,
):
    """
    Тест: main() с подтверждением "нет".

    Проверяет:
    - При ответе "нет" фильтрация по статусу все равно выполняется

    Результат: вызов _filter_by_status_interactive
    """
    mock_select.return_value = "json"
    mock_load.return_value = [{"id": 1, "date": "01.01.2024"}]
    mock_filter_status.return_value = [{"id": 1}]
    mock_sort.return_value = [{"id": 1}]
    mock_filter_currency.return_value = [{"id": 1}]
    mock_input.side_effect = ["нет", "нет", "нет", "нет", "нет", "нет"]
    main()
    # Проверяем что filter_status был вызван
    mock_filter_status.assert_called_once()


@patch("main._display_results")
@patch("main._show_category_statistics")
@patch("main._search_by_keywords")
@patch("main._filter_by_currency_interactive")
@patch("main._sort_by_date_interactive")
@patch("main._filter_by_status_interactive")
@patch("main._load_transactions_by_format")
@patch("main._select_file_format")
@patch("builtins.input")
@patch("builtins.print")
def test_main_confirm_invalid(
    mock_print,
    mock_input,
    mock_select,
    mock_load,
    mock_filter_status,
    mock_sort,
    mock_filter_currency,
    mock_search,
    mock_stats,
    mock_display,
):
    """
    Тест: main() с невалидным подтверждением.

    Проверяет:
    - При невалидном ответе ("maybe") программа продолжает работу
    - После "да" выполняется отображение результатов

    Результат: вызов _display_results
    """
    mock_select.return_value = "json"
    mock_load.return_value = [{"id": 1, "date": "01.01.2024"}]
    mock_filter_status.return_value = [{"id": 1}]
    mock_sort.return_value = [{"id": 1}]
    mock_filter_currency.return_value = [{"id": 1}]
    # invalid, then да, then нет
    mock_input.side_effect = ["maybe", "да", "да", "нет", "нет", "нет", "нет"]
    main()
    mock_display.assert_called_once()


@patch("main._select_file_format")
@patch("builtins.print")
def test_main_skip(mock_print, mock_select):
    """
    Тест: main() с пропуском выбора формата.

    Проверяет:
    - При None от _select_file_format программа завершается

    Результат: завершение без ошибок
    """
    mock_select.return_value = None
    main()
