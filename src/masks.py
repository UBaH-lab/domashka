# -*- coding: utf-8 -*-
"""
Модуль masks содержит функции для маскирования номеров карт/счетов
и преобразования дат в удобочитаемый формат.

Маскирование используется для:
- Защиты конфиденциальных данных при отображении
- Логирования без раскрытия полных номеров
- Отображения в UI с защитой персональных данных
"""

from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)


def mask_account_card(text: str) -> str:
    """
    Маскирует номер карты или счёта в тексте.

    Функция находит цифры в строке и заменяет их на маску,
    оставляя только последние 4 цифры для идентификации.

    Args:
        text (str): Строка, содержащая название и номер.
            Формат: "Название номер" или "Счет номер"

    Returns:
        str: Маскированная строка.
            - Для карт: "Префикс **** ****XXXX" (последние 4 цифры)
            - Для счетов: "Префикс **XXXX"
            - Без цифр: исходная строка
            - Пустая/None: возвращается как есть

    Examples:
        >>> mask_account_card("Visa Gold 5999414228426353")
        'Visa Gold **** ****6353'

        >>> mask_account_card("Счет 12345678901234567890")
        'Счет **7890'

        >>> mask_account_card("Без номера")
        'Без номера'

    Note:
        Функция использует регулярные выражения для поиска цифр
        и логирует все действия через модуль logging.
    """
    logger.debug(f"Маскирование: {text}")

    # Проверка на пустой или некорректный ввод
    if not isinstance(text, str) or text == "":
        logger.warning("Пустой или некорректный ввод для маскирования")
        return text

    # Ищем первую цифру в строке
    m = re.search(r"\d", text)
    if not m:
        logger.debug("В тексте нет цифр, возврат исходной строки")
        return text

    # Разделяем на префикс и цифры
    prefix_with_space = text[: m.start()]
    digits_only = re.sub(r"\D", "", text[m.start() :])

    if not digits_only:
        logger.warning("Не найдены цифры после извлечения")
        return text

    # Берем последние 4 цифры (или меньше, если цифр мало)
    last = digits_only[-4:] if len(digits_only) >= 4 else digits_only

    # Формируем результат в зависимости от типа
    if text.strip().startswith("Счет"):
        result = prefix_with_space + "**" + last
        logger.info(f"Маскировка счёта: {text} -> {result}")
        return result

    result = prefix_with_space + "**** ****" + last
    logger.info(f"Маскировка карты: {text} -> {result}")
    return result


def get_date(text: str) -> str:
    """
    Преобразует дату из ISO-формата в DD.MM.YYYY.

    Поддерживает несколько форматов ISO даты и времени.

    Args:
        text (str): Строка с датой в ISO-формате.
            Поддерживаемые форматы:
            - "2024-03-11T12:34:56.123456" (с микросекундами)
            - "2024-03-11T12:34:56" (без микросекунд)
            - "2024-03-11" (только дата)

    Returns:
        str: Дата в формате DD.MM.YYYY.
            Пример: "11.03.2024"

    Raises:
        ValueError: Если аргумент не строка или формат неверен.

    Examples:
        >>> get_date("2024-03-11T12:34:56.123456")
        '11.03.2024'

        >>> get_date("2024-03-11T12:34:56")
        '11.03.2024'

        >>> get_date("2024-03-11")
        '11.03.2024'

        >>> get_date("invalid")
        ValueError: Invalid date format

    Note:
        Функция пробует форматы по порядку, от наиболее полных
        к простым. Время игнорируется, используется только дата.
    """
    logger.debug(f"Преобразование даты: {text}")

    # Проверка типа аргумента
    if not isinstance(text, str):
        logger.error("Дата должна быть строкой")
        raise ValueError("Date must be a string")

    # Список поддерживаемых форматов (от полных к простым)
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",  # С микросекундами
        "%Y-%m-%dT%H:%M:%S",  # Без микросекунд
        "%Y-%m-%d",  # Только дата
    ]

    # Пробуем каждый формат
    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            result = dt.strftime("%d.%m.%Y")
            logger.info(f"Преобразование даты: {text} -> {result}")
            return result
        except ValueError:
            continue

    # Ни один формат не подошел
    logger.error(f"Неверный формат даты: {text}")
    raise ValueError("Invalid date format")


# Псевдоним для совместимости
get_mask_card_number = mask_account_card

__all__ = ["mask_account_card", "get_date", "get_mask_card_number"]
