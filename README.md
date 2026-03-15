# Учебный проект: Фича для личного кабинета клиента банка

Данный репозиторий реализует базовые функции личного кабинета банковского клиента:
- маскировку номеров карт и счетов
- фильтрацию данных по статусу
- сортировку по датам
- валидацию и преобразование дат
- чтение финансовых транзакций из CSV и Excel файлов

Тесты покрывают ключевые сценарии работы функций.

---

## Оглавление

- [Описание проекта](#описание-проекта)
- [Требования](#требования)
- [Установка](#установка)
  - [Клонирование репозитория](#клонирование-репозитория)
  - [Установка зависимостей](#установка-зависимостей)
- [Запуск проекта](#запуск-проекта)
- [Модули и их описание](#модули-и-их-описание)
  - [processing](#processing)
  - [masks](#masks)
  - [widget](#widget)
  - [transactions_reader](#transactions_reader)
  - [generators](#generators)
  - [decorators](#decorators)
- [Тестирование](#тестирование)
  - [Что проверяют тесты](#что-проверяют-тесты)
  - [Как запускать тесты](#как-запускать-тесты)
  - [Проверка покрытия тестами](#проверка-покрытия-тестами)
- [Примеры использования](#примеры-использования)
- [Структура проекта](#структура-проекта)
- [Частые вопросы (FAQ)](#частые-вопросы-faq)
- [Лицензия и контакты](#лицензия-и-контакты)

---

## Описание проекта

Фича предоставляет набор функций, необходимых для работы личного кабинета банковского клиента:
- маскировка номеров карт и счетов
- фильтрация данных по статусу транзакций
- сортировка транзакций по дате
- валидация и преобразование дат в формат DD.MM.YYYY
- чтение финансовых транзакций из CSV и Excel файлов

Поддерживаемые модули:
- processing
- masks
- widget
- transactions_reader
- generators
- decorators

Также включены автоматические тесты для проверки корректности работы функций.

---

## Требования

- Python версии >= 3.13
- pip
- (по необходимости) Poetry

---

## Установка

### Клонирование репозитория

```bash
git clone <URL_репозитория>
cd <имя_проекта>
Установка зависимостей
Вариант с Poetry (рекомендуется)
```

```bash
poetry install
poetry shell
poetry run python main.py
Вариант через requirements.txt
```

```bash
pip install -r requirements.txt
```
Запуск проекта
Обычный запуск:

```bash
python main.py
```
С использованием Poetry:

```bash
poetry run python main.py
```
Примечание: команды могут зависеть от настроек проекта.

Модули и их описание

processing
filter_by_state(items: list, state_value: str | None = None) -> list

Фильтрует список словарей по ключу state.
Если state_value равен None, возвращает копию исходного списка.
sort_by_date(transactions: list, ascending: bool = True) -> list

Возвращает новый список транзакций, отсортированный по полю date.
ascending True: oldest first; ascending False: newest first.
masks
get_mask_card_number(card_number: str) -> str

Маскирует номер карты, показывая первые 6 и последние 4 цифры.
Пример: вход "1234567890123456" -> маскированное "123456******3456".
get_mask_account(account_number: str) -> str

Маскирует номер счета: показывает последние 4 цифры, перед ними две звездочки.
Пример: вход "1234567890123456" -> "**3456"
widget
mask_account_card(item_type: str, number: str) -> str
В зависимости от типа:
"card" вызывает get_mask_card_number
"account" вызывает get_mask_account
Возвращает строку с маскированным номером.
При неверном типе выбрасывает исключение ValueError.
transactions_reader
read_transactions_csv(file_path: str | Path) -> List[Dict[str, Any]]

Считывает финансовые транзакции из CSV-файла.
Принимает путь к файлу CSV в качестве аргумента.
Возвращает список словарей с транзакциями.
Выбрасывает FileNotFoundError, если файл не существует.
Выбрасывает ValueError, если файл пустой или имеет неверный формат.
read_transactions_excel(file_path: str | Path) -> List[Dict[str, Any]]

Считывает финансовые транзакции из XLSX-файла.
Принимает путь к файлу Excel в качестве аргумента.
Возвращает список словарей с транзакциями.
Выбрасывает FileNotFoundError, если файл не существует.
Выбрасывает ValueError, если файл пустой или имеет неверный формат.
read_transactions(file_path: str | Path) -> List[Dict[str, Any]]

Универсальная функция для чтения транзакций из файла.
Автоматически определяет формат по расширению файла (.csv, .xlsx, .xls).
Возвращает список словарей с транзакциями.
Выбрасывает ValueError, если формат файла не поддерживается.
generators
filter_by_currency(transactions: List[Dict], currency_code: str) -> Iterator[Dict]

Возвращает итератор по транзакциям с указанной валютой.
transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]

Генерирует описания транзакций.
card_number_generator(start: int = 1, end: int = 9999999999999999) -> Generator[str, None, None]

Генерирует номера карт в формате XXXX XXXX XXXX XXXX по диапазону.
decorators
log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]
Декоратор логирования для функций.
Логирует начало выполнения, успешное завершение и ошибки.
Если указан filename — логи пишутся в файл, иначе в консоль.
Исключения повторно возбуждаются после логирования.
Тестирование
Что проверяют тесты
Модуль masks

get_mask_card_number: корректность маскировки карт разных форматов и обработка некорректных данных.
get_mask_account: корректность маскировки номеров счетов разной длины и форматов.
Модуль widget

mask_account_card: корректная маскировка по типу (карта или счет), обработка ошибок и некорректных данных.
Общие функции

filter_by_state: фильтрация данных по состоянию.
sort_by_date: сортировка по дате.
get_date: преобразование даты из ISO в формат DD.MM.YYYY.
Модуль transactions_reader

read_transactions_csv: успешное чтение CSV-файлов, обработка несуществующих файлов, пустых файлов и файлов с неверным форматом.
read_transactions_excel: успешное чтение Excel-файлов, обработка несуществующих файлов и пустых файлов.
read_transactions: автоматическое определение формата файла, обработка неподдерживаемых форматов.
Все тесты используют Mock и patch для изоляции от файловой системы.
Модуль generators

filter_by_currency: фильтрация транзакций по валюте.
transaction_descriptions: генерация описаний транзакций.
card_number_generator: генерация номеров карт в заданном диапазоне.
Модуль decorators

log: логирование в консоль и в файл, обработка успешного выполнения и ошибок.
Как запускать тесты
Установить pytest:

```bash
pip install pytest
```
Запуск всех тестов:

```
pytest
```
Запуск тестов с подробным выводом:

```bash
pytest -v
```
Запуск тестов по конкретному файлу:

```bash
pytest test_transactions_reader.py
```
Запуск тестов с покрытием:

```bash
pytest --cov=transactions_reader --cov-report=term-missing
```
Проверка покрытия тестами
Для проверки покрытия тестами выполните команду:

```bash
pytest --cov=src --cov-report=term-missing
```
Требуемое покрытие: не менее 80%.

Примеры использования
Фильтрация по состоянию

python

from src.processing import filter_by_state

data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}]
filtered = filter_by_state(data, "EXECUTED")
Сортировка по дате
python

from src.processing import sort_by_date

transactions = [
    {"id": 1, "date": "2020-01-02T12:00:00"},
    {"id": 2, "date": "2019-12-31T23:59:59"},
]
sorted_list = sort_by_date(transactions, ascending=True)
Маскировка номера карты
python

from src.masks import get_mask_card_number

masked = get_mask_card_number("1234567890123456")
Маскировка номера счета
python

from src.masks import get_mask_account

masked = get_mask_account("1234567890123456")
Маскировка через виджет
python

from src.widget import mask_account_card

masked = mask_account_card("card", "1234567890123456")
Чтение транзакций из CSV
python

from src.transactions_reader import read_transactions_csv

transactions = read_transactions_csv("transactions.csv")
print(f"Прочитано {len(transactions)} транзакций")
Чтение транзакций из Excel
python

from src.transactions_reader import read_transactions_excel

transactions = read_transactions_excel("transactions_excel.xlsx")
print(f"Прочитано {len(transactions)} транзакций")
Универсальное чтение транзакций
python

from src.transactions_reader import read_transactions

# Автоматическое определение формата
csv_transactions = read_transactions("transactions.csv")
excel_transactions = read_transactions("transactions_excel.xlsx")
Использование генераторов
python

from src import generators

transactions = [...]  # список транзакций

# Получение транзакций в USD
usd_transactions = generators.filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

# Получение описаний транзакций
descriptions = generators.transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))

# Генерация номеров карт
for card in generators.card_number_generator(1, 3):
    print(card)
Использование декоратора логирования
python

from src.decorators import log

@log(filename="logs.txt")
def transfer_funds(amount, to_account):
    # логика перевода
    return True

transfer_funds(100, "ACC12345")
Структура проекта

src/
├── processing/
│   └── __init__.py          # функции filter_by_state, sort_by_date
├── masks/
│   └── __init__.py          # функции get_mask_card_number, get_mask_account
├── widget/
│   └── __init__.py          # функция mask_account_card
├── transactions_reader/
│   └── __init__.py          # функции read_transactions_csv, read_transactions_excel, read_transactions
├── generators/
│   └── __init__.py          # функции filter_by_currency, transaction_descriptions, card_number_generator
└── decorators/
    └── log.py               # декоратор log

tests/
├── test_processing.py       # тесты модуля processing
├── test_masks.py            # тесты модуля masks
├── test_widget.py           # тесты модуля widget
├── test_transactions_reader.py  # тесты модуля transactions_reader
├── test_generators.py       # тесты модуля generators
└── test_decorators.py       # тесты модуля decorators

main.py
conftest.py                  # общий набор фикстур для тестов
requirements.txt             # зависимости проекта
README.md                    # документация проекта
.gitignore                   # игнорируемые файлы
Частые вопросы (FAQ)
В каком формате должны быть даты?
Поддерживаются ISO-строки и их вариации, а также формат DD.MM.YYYY для вывода. При неверном формате функция должна поднимать исключение (ValueError).

Что делать, если номер карты или счета некорректен?
Функции должны возвращать логичные значения или выбрасывать исключения в зависимости от реализации. Обычно используется ValueError для некорректного формата.

Как расширять тесты?
Добавляйте новые кейсы в параметризованные тесты, следуя существующей структуре и описаниям. Для модуля transactions_reader используйте Mock и patch для изоляции от файловой системы.

Какие форматы файлов поддерживаются для чтения транзакций?
Поддерживаются CSV (.csv) и Excel (.xlsx, .xls) файлы. Функция read_transactions автоматически определяет формат по расширению файла.

Что делать, если файл с транзакциями не найден?
Функции read_transactions_csv и read_transactions_excel выбрасывают FileNotFoundError. Обрабатывайте это исключение в вашем коде.

Как проверить покрытие тестами?
Используйте команду pytest --cov=src --cov-report=term-missing для проверки покрытия. Требуемое покрытие — не менее 80%.

Лицензия и контакты
Лицензия:

Контакты: