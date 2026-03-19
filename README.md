🏦 Учебный проект: Фича для личного кабинета клиента банка
Данный репозиторий реализует полнофункциональный личный кабинет банковского клиента с расширенными возможностями:

- 📋 Интерактивный CLI-интерфейс для работы с транзакциями
- 🎭 Маскировку номеров карт и счетов
- 🔍 Фильтрацию данных по статусу, валюте и ключевым словам
- 📅 Сортировку по датам
- 📊 Чтение транзакций из JSON, CSV и Excel файлов
- 🔎 Поиск по транзакциям по ключевым словам
- 📈 Подсчёт операций по категориям
- 🧪 Комплексное тестирование с покрытием >80%

## Оглавление

- [Описание проекта](#описание-проекта)
- [Требования](#требования)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Модули и их описание](#модули-и-их-описание)
- [Тестирование](#тестирование)
- [Примеры использования](#примеры-использования)
- [Структура проекта](#структура-проекта)
- [Частые вопросы (FAQ)](#частые-вопросы-faq)
- [Лицензия и контакты](#лицензия-и-контакты)

## Описание проекта

Фича предоставляет полнофункциональный набор инструментов для работы с банковскими транзакциями.

### Основные возможности

| Функция | Описание |
|---------|----------|
| Загрузка данных | Чтение транзакций из JSON, CSV, XLSX файлов |
| Фильтрация | По статусу (EXECUTED, CANCELED, PENDING), валюте, ключевым словам |
| Сортировка | По дате (по возрастанию или убыванию) |
| Маскировка | Скрытие номеров карт и счетов для безопасности |
| Поиск | Поиск транзакций по ключевым словам в описании |
| Категоризация | Подсчёт операций по категориям |
| Форматирование | Красивый вывод транзакций в консоль |

### Интерактивный интерфейс

Программа предоставляет дружественный CLI-интерфейс с пошаговым выбором:

1. Выбор файла с транзакциями
2. Выбор формата файла (JSON, CSV, XLSX)
3. Фильтрация по статусу
4. Фильтрация по валюте
5. Сортировка по дате
6. Поиск по ключевым словам
7. Подсчёт по категориям

## Требования

### Системные требования

| Компонент | Версия |
|-----------|--------|
| Python | >= 3.13 |
| pip | последняя версия |
| Poetry | (опционально) |

### Необходимые библиотеки

pandas>=2.0.0 openpyxl>=3.1.0 pytest>=7.0.0 pytest-cov>=4.0.0 pytest-mock>=3.10.0



## Установка

### Клонирование репозитория

```bash
git clone <URL_репозитория>
```
cd <имя_проекта>
Установка зависимостей
Вариант с Poetry (рекомендуется)
```bash

# Установка всех зависимостей
poetry install

# Активация виртуального окружения
poetry shell

# Запуск программы
poetry run python main.py
```
Вариант через requirements.txt
```bash

# Установка зависимостей
pip install -r requirements.txt

# Запуск программы
python main.py
```
Запуск проекта
Обычный запуск
```bash

python main.py
```
Запуск с Poetry
```bash

poetry run python main.py
```
Пример работы программы

Программа: Привет! Добро пожаловать в программу по работе с банковскими транзакциями.
Программа: Выберите необходимый файл с транзакциями.
Программа: Введите название файла в формате: filename.extension
Пользователь: operations.json

Программа: Введите статус для фильтрации.
Доступные статусы: EXECUTED, CANCELED, PENDING
Пользователь: EXECUTED

Программа: Операции отфильтрованы по статусу "EXECUTED"

Программа: Нужна ли сортировка по дате? (да/нет)
Пользователь: да

Программа: Отсортировать по возрастанию или убыванию?
Пользователь: убывание
Модули и их описание
main
Главный модуль с интерактивным интерфейсом и функциями обработки транзакций.

Функции загрузки данных
load_transactions_from_json
python

load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]
Описание: Загружает транзакции из JSON-файла.

Параметры:

file_path — путь к JSON-файлу с транзакциями
Возвращает: Список словарей с транзакциями или пустой список при ошибке.

Исключения: Не выбрасывает, все ошибки обрабатываются внутри.

Пример:

python

from main import load_transactions_from_json

data = load_transactions_from_json("operations.json")
print(f"Загружено: {len(data)} транзакций")
load_transactions_from_csv
python

load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]
Описание: Загружает транзакции из CSV-файла.

Параметры:

file_path — путь к CSV-файлу с транзакциями
Возвращает: Список словарей с транзакциями.

Пример:

python

from main import load_transactions_from_csv

data = load_transactions_from_csv("transactions.csv")
load_transactions_from_excel
python

load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]
Описание: Загружает транзакции из XLSX-файла.

Параметры:

file_path — путь к Excel-файлу с транзакциями
Возвращает: Список словарей с транзакциями.

Пример:

python

from main import load_transactions_from_excel

data = load_transactions_from_excel("report.xlsx")
Функции фильтрации и сортировки
get_valid_status
python

get_valid_status() -> Optional[str]
Описание: Запрашивает у пользователя статус транзакции с валидацией.

Возвращает: Валидный статус из списка STATUSES ("EXECUTED", "CANCELED", "PENDING").

Пример:

python

from main import get_valid_status

status = get_valid_status()  # Интерактивный ввод
filter_by_status
python

filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]
Описание: Фильтрует транзакции по статусу.

Параметры:

data — список транзакций для фильтрации
status — статус для фильтрации ("EXECUTED", "CANCELED", "PENDING")
Возвращает: Отфильтрованный список транзакций.

Пример:

python

from main import filter_by_status

transactions = [
    {"id": 1, "state": "EXECUTED"},
    {"id": 2, "state": "CANCELED"},
]
filtered = filter_by_status(transactions, "EXECUTED")
# Результат: [{"id": 1, "state": "EXECUTED"}]
sort_by_date
python

sort_by_date(data: List[Dict[str, Any]], ascending: bool = False) -> List[Dict[str, Any]]
Описание: Сортирует транзакции по дате.

Параметры:

data — список транзакций для сортировки
ascending — порядок сортировки:
True — по возрастанию (старые сначала)
False — по убыванию (новые сначала, по умолчанию)
Возвращает: Отсортированный список транзакций.

Пример:

python

from main import sort_by_date

transactions = [
    {"date": "15.06.2024", "id": 2},
    {"date": "01.01.2024", "id": 1},
    {"date": "31.12.2024", "id": 3},
]

# По убыванию (новые сначала)
sorted_desc = sort_by_date(transactions)
# Результат: [id=3, id=2, id=1]

# По возрастанию (старые сначала)
sorted_asc = sort_by_date(transactions, ascending=True)
# Результат: [id=1, id=2, id=3]
filter_by_currency
python

filter_by_currency(data: List[Dict[str, Any]], currency: str = "RUB") -> List[Dict[str, Any]]
Описание: Фильтрует транзакции по валюте.

Параметры:

data — список транзакций
currency — код валюты ISO 4217 (по умолчанию "RUB")
Возвращает: Список транзакций в указанной валюте.

Пример:

python

from main import filter_by_currency

transactions = [
    {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
    {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
]

rub_transactions = filter_by_currency(transactions, "RUB")
Функции маскировки и форматирования
mask_number
python

mask_number(number: str) -> str
Описание: Маскирует номер карты или счёта.

Параметры:

number — номер карты (16 цифр) или счёта (>16 цифр)
Возвращает: Маскированный номер.

Логика:

16 цифр → маскировка как карта: 1234 56** **** 3456
16 цифр → маскировка как счёт: **7890

Пример:

python

from main import mask_number

card = mask_number("1234567890123456")
# Результат: "1234 56** **** 3456"

account = mask_number("12345678901234567890")
# Результат: "**7890"
format_transaction
python

format_transaction(transaction: Dict[str, Any]) -> str
Описание: Форматирует транзакцию для вывода в консоль.

Параметры:

transaction — словарь с данными транзакции
Возвращает: Отформатированная строка для вывода.

Пример:

python

from main import format_transaction

transaction = {
    "date": "15.06.2024",
    "description": "Перевод",
    "from": "Счёт 12345678901234567890",
    "to": "Карта 1234567890123456",
    "operationAmount": {
        "amount": 1000,
        "currency": {"code": "RUB"}
    }
}

print(format_transaction(transaction))
# Вывод:
# 15.06.2024 Перевод
# Счёт **7890 -> Карта 1234 56** **** 3456
# Сумма: 1000 руб.
ask_yes_no
python

ask_yes_no(prompt: str) -> bool
Описание: Запрашивает у пользователя ответ да/нет.

Параметры:

prompt — текст вопроса
Возвращает: True если "да", False если "нет".

Допустимые ответы:

Да: "да", "yes", "y", "д"
Нет: "нет", "no", "n", "н"
Пример:

python

from main import ask_yes_no

if ask_yes_no("Продолжить?"):
    print("Продолжаем...")
bank_utils
Модуль для поиска и категоризации транзакций.

process_bank_search
python

process_bank_search(data: List[Dict[str, Any]], search_query: str) -> List[Dict[str, Any]]
Описание: Ищет транзакции по ключевым словам в описании.

Параметры:

data — список транзакций для поиска
search_query — поисковый запрос (слово или фраза)
Возвращает: Список транзакций, содержащих запрос в описании.

Особенности:

Поиск не зависит от регистра
Ищет частичные совпадения
Пример:

python

from bank_utils import process_bank_search

transactions = [
    {"id": 1, "description": "Перевод на карту"},
    {"id": 2, "description": "Оплата услуг"},
    {"id": 3, "description": "Перевод на счёт"},
]

result = process_bank_search(transactions, "перевод")
# Результат: [{"id": 1, ...}, {"id": 3, ...}]
process_bank_operations
python

process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]
Описание: Подсчитывает количество транзакций по категориям.

Параметры:

data — список транзакций
categories — список категорий для подсчёта
Возвращает: Словарь {категория: количество}.

Пример:

python

from bank_utils import process_bank_operations

transactions = [
    {"description": "Перевод на карту"},
    {"description": "Оплата услуг"},
    {"description": "Перевод на счёт"},
    {"description": "Снятие наличных"},
]

result = process_bank_operations(transactions, ["перевод", "оплата", "снятие"])
# Результат: {"перевод": 2, "оплата": 1, "снятие": 1}
processing
Модуль для базовой обработки данных.

filter_by_state
python

filter_by_state(items: list, state_value: str | None = None) -> list
Описание: Фильтрует список словарей по ключу state.

Параметры:

items — список словарей
state_value — значение для фильтрации (если None, возвращает копию списка)
Пример:

python

from src.processing import filter_by_state

data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}]
filtered = filter_by_state(data, "EXECUTED")
sort_by_date
python

sort_by_date(transactions: list, ascending: bool = True) -> list
Описание: Возвращает новый список транзакций, отсортированный по полю date.

Параметры:

transactions — список транзакций
ascending — True: старые сначала; False: новые сначала
Пример:

python

from src.processing import sort_by_date

transactions = [
    {"id": 1, "date": "2020-01-02T12:00:00"},
    {"id": 2, "date": "2019-12-31T23:59:59"},
]
sorted_list = sort_by_date(transactions, ascending=True)
masks
Модуль для маскировки номеров карт и счетов.

get_mask_card_number
python

get_mask_card_number(card_number: str) -> str
Описание: Маскирует номер карты, показывая первые 6 и последние 4 цифры.

Пример:

python

from src.masks import get_mask_card_number

masked = get_mask_card_number("1234567890123456")
# Результат: "123456******3456"
get_mask_account
python

get_mask_account(account_number: str) -> str
Описание: Маскирует номер счета, показывая последние 4 цифры.

Пример:

python

from src.masks import get_mask_account

masked = get_mask_account("1234567890123456")
# Результат: "**3456"
widget
Модуль виджета для маскировки.

mask_account_card
python

mask_account_card(item_type: str, number: str) -> str
Описание: Маскирует номер в зависимости от типа.

Параметры:

item_type — "card" или "account"
number — номер для маскировки
Исключения: ValueError при неверном типе.

Пример:

python

from src.widget import mask_account_card

masked_card = mask_account_card("card", "1234567890123456")
masked_account = mask_account_card("account", "1234567890123456")
transactions_reader
Модуль для чтения транзакций из файлов.

read_transactions_csv
python

read_transactions_csv(file_path: str | Path) -> List[Dict[str, Any]]
Описание: Считывает транзакции из CSV-файла.

Исключения:

FileNotFoundError — файл не существует
ValueError — файл пустой или неверный формат
Пример:

python

from src.transactions_reader import read_transactions_csv

transactions = read_transactions_csv("transactions.csv")
read_transactions_excel
python

read_transactions_excel(file_path: str | Path) -> List[Dict[str, Any]]
Описание: Считывает транзакции из XLSX-файла.

Пример:

python

from src.transactions_reader import read_transactions_excel

transactions = read_transactions_excel("transactions_excel.xlsx")
read_transactions
python

read_transactions(file_path: str | Path) -> List[Dict[str, Any]]
Описание: Универсальная функция для чтения транзакций. Автоматически определяет формат по расширению.

Поддерживаемые форматы: .csv, .xlsx, .xls

Пример:

python

from src.transactions_reader import read_transactions

csv_transactions = read_transactions("transactions.csv")
excel_transactions = read_transactions("transactions.xlsx")
generators
Модуль с генераторами для эффективной обработки данных.

filter_by_currency
python

filter_by_currency(transactions: List[Dict], currency_code: str) -> Iterator[Dict]
Описание: Возвращает итератор по транзакциям с указанной валютой.

Пример:

python

from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))
transaction_descriptions
python

transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]
Описание: Генерирует описания транзакций.

Пример:

python

from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
card_number_generator
python

card_number_generator(start: int = 1, end: int = 9999999999999999) -> Generator[str, None, None]
Описание: Генерирует номера карт в формате XXXX XXXX XXXX XXXX.

Пример:

python

from src.generators import card_number_generator

for card in card_number_generator(1, 3):
    print(card)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
decorators
Модуль с декораторами для логирования.

log
python

log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]
Описание: Декоратор логирования для функций.

Параметры:

filename — путь к файлу логов (если None, вывод в консоль)
Функционал:

Логирует начало выполнения
Логирует успешное завершение
Логирует ошибки с трейсбеком
Пример:

python

from src.decorators import log

@log(filename="logs.txt")
def transfer_funds(amount, to_account):
    return True

transfer_funds(100, "ACC12345")
Тестирование
Что проверяют тесты
tests/test_main.py
Класс тестов	Что проверяется
TestLoadTransactionsFromJson	Загрузка JSON (валидный, пустой, отсутствующий, некорректный, с кириллицей)
TestLoadTransactionsFromCsv	Загрузка CSV (валидный, пустой, ошибки)
TestLoadTransactionsFromExcel	Загрузка XLSX (валидный, ошибки)
TestGetValidStatus	Валидация статуса (корректный, нижний регистр, повторный ввод)
TestFilterByStatus	Фильтрация по статусу (EXECUTED, CANCELED, PENDING, без совпадений, пустой список)
TestSortByDate	Сортировка (по убыванию, по возрастанию, одинаковые даты, отсутствующая дата)
TestFilterByCurrency	Фильтрация по валюте (RUB, USD, разные валюты, отсутствующее поле)
TestMaskNumber	Маскировка номеров (карта 16 цифр, счёт >16 цифр, с пробелами, с префиксом, пустая строка)
TestFormatTransaction	Форматирование вывода (полная транзакция, без from, без to)
TestAskYesNo	Ввод да/нет (разные варианты ответов)
TestProcessBankSearch	Поиск по ключевым словам
TestProcessBankOperations	Подсчёт по категориям
tests/test_masks.py
Класс тестов	Что проверяется
TestGetMaskCardNumber	Маскировка номера карты
TestGetMaskAccount	Маскировка номера счёта
tests/test_processing.py
Класс тестов	Что проверяется
TestFilterByState	Фильтрация по состоянию
TestSortByDate	Сортировка по дате
tests/test_widget.py
Класс тестов	Что проверяется
TestMaskAccountCard	Маскировка карт и счетов
tests/test_transactions_reader.py
Класс тестов	Что проверяется
TestReadTransactionsCsv	Чтение CSV файлов
TestReadTransactionsExcel	Чтение Excel файлов
TestReadTransactions	Универсальное чтение
tests/test_generators.py
Класс тестов	Что проверяется
TestFilterByCurrency	Генератор фильтрации по валюте
TestTransactionDescriptions	Генератор описаний
TestCardNumberGenerator	Генератор номеров карт
tests/test_decorators.py
Класс тестов	Что проверяется
TestLogDecorator	Логирование в файл и консоль
Запуск тестов
bash

# Все тесты
pytest

# С покрытием
pytest --cov=src --cov-report=html

# Конкретный файл
pytest tests/test_main.py -v
Примеры использования
Полный цикл работы
python

from main import (
    load_transactions_from_json,
    filter_by_status,
    sort_by_date,
    format_transaction
)

# 1. Загрузка
data = load_transactions_from_json("operations.json")

# 2. Фильтрация
executed = filter_by_status(data, "EXECUTED")

# 3. Сортировка
sorted_data = sort_by_date(executed, ascending=False)

# 4. Вывод
for t in sorted_data[:5]:
    print(format_transaction(t))
Использование генераторов
python

from src.generators import filter_by_currency, card_number_generator

# Фильтрация по валюте (ленивая)
usd_gen = filter_by_currency(transactions, "USD")
first_usd = next(usd_gen)

# Генерация номеров карт
for card in card_number_generator(1, 5):
    print(card)
Структура проекта

PythonProject19/
├── src/
│   ├── masks.py              # Маскировка номеров
│   ├── processing.py         # Фильтрация и сортировка
│   ├── widget.py             # Виджеты
│   ├── transactions_reader.py # Чтение файлов
│   ├── generators.py         # Генераторы
│   └── decorators.py         # Декораторы
├── tests/
│   ├── test_main.py
│   ├── test_masks.py
│   ├── test_processing.py
│   ├── test_widget.py
│   ├── test_transactions_reader.py
│   ├── test_generators.py
│   └── test_decorators.py
├── main.py                   # Точка входа
├── README.md
├── requirements.txt
└── pyproject.toml
Частые вопросы (FAQ)
Q: Как добавить новый формат файла?

A: Реализуйте функцию load_transactions_from_<format> в main.py и добавьте обработку расширения.

Q: Как изменить маску?

A: Отредактируйте функции в src/masks.py.

Q: Поддерживается ли асинхронность?

A: Нет, текущая версия синхронная.

Q: Как запустить только определённые тесты?

A: Используйте pytest tests/test_main.py::TestFilterByStatus -v для конкретного класса.

Лицензия и контакты
Лицензия: MIT License

Автор: Ivan

Email: ubahyska1992@gmail.com


