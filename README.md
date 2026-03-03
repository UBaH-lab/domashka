# Учебный проект: Фича для личного кабинета клиента банка

Данный репозиторий реализует базовые функции личного кабинета банковского клиента:
- маскировку номеров карт и счетов
- фильтрацию данных по статусу
- сортировку по датам
- валидацию и преобразование дат

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
- [Тестирование](#тестирование)
  - [Что проверяют тесты](#что-проверяют-тесты)
  - [Как запускать тесты](#как-запускать-тесты)
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

Поддерживаемые модули:
- processing
- masks
- widget

Также включены автоматические тесты для проверки корректности работы функций.

---

## Требования

- Python версии >= 3.13
- pip
- (по необходимости) Poetry

---

## Установка

### Клонирование репозитория

- git clone <URL_репозитория>
- cd <имя_проекта>

### Установка зависимостей

#### Вариант с Poetry (рекомендуется)
- poetry install
- poetry shell
- poetry run python main.py

#### Вариант через requirements.txt
- pip install -r requirements.txt

---

## Запуск проекта

- Обычный запуск:
  - python main.py

- С использованием Poetry:
  - poetry run python main.py

Примечание: команды могут зависеть от настроек проекта.

---

## Модули и их описание

### processing
- filter_by_state(items: list, state_value: str | None = None) -> list
  - Фильтрует список словарей по ключу `state`.
  - Если `state_value` равен None, возвращает копию исходного списка.

- sort_by_date(transactions: list, ascending: bool = True) -> list
  - Возвращает новый список транзакций, отсортированный по полю `date`.
  - ascending True: oldest first; ascending False: newest first.

### masks
- get_mask_card_number(card_number: str) -> str
  - Маскирует номер карты, показывая первые 6 и последние 4 цифры.
  - Пример: вход "1234567890123456" -> маскированное "123456******3456" (формат зависит от реализации).

- get_mask_account(account_number: str) -> str
  - Маскирует номер счета: показывает последние 4 цифры, перед ними две звездочки.
  - Пример: вход "1234567890123456" -> "**3456"

### widget
- mask_account_card(item_type: str, number: str) -> str
  - В зависимости от типа:
    - "card" вызывает get_mask_card_number
    - "account" вызывает get_mask_account
  - Возвращает строку с маскированным номером.
  - При неверном типе выбрасывает исключение ValueError.

---

## Тестирование

### Что проверяют тесты

- Модуль masks
  - get_mask_card_number: корректность маскировки карт разных форматов и обработка некорректных данных.
  - get_mask_account: корректность маскировки номеров счетов разной длины и форматов.

- Модуль widget
  - mask_account_card: корректная маскировка по типу (карта или счет), обработка ошибок и некорректных данных.

- Общие функции
  - filter_by_state: фильтрация данных по состоянию.
  - sort_by_date: сортировка по дате.
  - get_date: преобразование даты из ISO в формат DD.MM.YYYY.

---

### Как запускать тесты

- Установить pytest:
  - pip install pytest

- Запуск тестов:
  - pytest

- По мере необходимости можно запустить тесты по файлу:
  - pytest test_module.py

---

## Примеры использования

- Фильтрация по состоянию
```python
from src.processing import filter_by_state

data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}]
filtered = filter_by_state(data, "EXECUTED")
```
Сортировка по дате
```python

from src.processing import sort_by_date

transactions = [
    {"id": 1, "date": "2020-01-02T12:00:00"},
    {"id": 2, "date": "2019-12-31T23:59:59"},
]
sorted_list = sort_by_date(transactions, ascending=True)
```
Маскировка номера карты
```python

from src.masks import get_mask_card_number

masked = get_mask_card_number("1234567890123456")
```
Маскировка номера счета
```python

from src.masks import get_mask_account

masked = get_mask_account("1234567890123456")
```
Маскировка через виджет
```python

from src.widget import mask_account_card

masked = mask_account_card("card", "1234567890123456")
```
### Структура проекта
*src/
1. processing/
содержит функции filter_by_state, sort_by_date
2. masks/
содержит get_mask_card_number, get_mask_account
3. widget/
содержит mask_account_card
* tests/
тесты по модулям processing, masks, widget
main.py
conftest.py (если нужен общий набор фикстур для тестов)
Частые вопросы (FAQ)
В каком формате должны быть даты?

Поддерживаются ISO-строки и их вариации, а также формат DD.MM.YYYY для вывода. При неверном формате функция должна поднимать исключение (ValueError).
Что делать, если номер карты или счета некорректен?

Функции должны возвращать логичные значения или выбрасывать исключения в зависимости от реализации. Обычно используется ValueError для некорректного формата.
Как расширять тесты?

## Модуль `generators`

Этот модуль содержит функции для обработки данных транзакций с помощью генераторов.

### Основные функции

- `filter_by_currency(transactions: List[Dict], currency_code: str) -> Iterator[Dict]`  
  Возвращает итератор по транзакциям с указанной валютой.

- `transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]`  
  Генерирует описания транзакций.

- `card_number_generator(start: int = 1, end: int = 9999999999999999) -> Generator[str, None, None]`  
  Генерирует номера карт в формате XXXX XXXX XXXX XXXX по диапазону.

### Примеры использования

```python
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
```
    

Добавляйте новые кейсы в параметризованные тесты, следуя существующей структуре и описаниям.
Лицензия и контакты
Лицензия: 
Контакты: 
