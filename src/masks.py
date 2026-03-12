"""
Модуль masks содержит функции для маскирования номера карты/счета и
преобразования даты в удобочитаемый формат.
"""

from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)


def mask_account_card(text: str) -> str:
    """
    Маскирует текст, содержащий номер карты или счёт.

    Правила:
    - Карты: префикс + "**** ****" + последние 4 цифры
    - Счета: префикс + "**" + последние 4 цифры
    - Если цифр нет, возвращает исходную строку.
    """
    logger.debug(f"Маскирование: {text}")

    if not isinstance(text, str) or text == "":
        logger.warning("Пустой или некорректный ввод для маскирования")
        return text

    m = re.search(r"\d", text)
    if not m:
        logger.debug("В тексте нет цифр, возврат исходной строки")
        return text

    prefix_with_space = text[: m.start()]
    digits_only = re.sub(r"\D", "", text[m.start() :])

    if not digits_only:
        logger.warning("Не найдены цифры после извлечения")
        return text

    last = digits_only[-4:] if len(digits_only) >= 4 else digits_only

    if text.strip().startswith("Счет"):
        result = prefix_with_space + "**" + last
        logger.info(f"Маскировка счёта: {text} -> {result}")
        return result

    result = prefix_with_space + "**** ****" + last
    logger.info(f"Маскировка карты: {text} -> {result}")
    return result


def get_date(text: str) -> str:
    """
    Преобразует дату в формате ISO-like в строку DD.MM.YYYY.
    При неверном формате возбуждает ValueError.
    """
    logger.debug(f"Преобразование даты: {text}")

    if not isinstance(text, str):
        logger.error("Дата должна быть строкой")
        raise ValueError("Date must be a string")

    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            result = dt.strftime("%d.%m.%Y")
            logger.info(f"Преобразование даты: {text} -> {result}")
            return result
        except ValueError:
            continue

    logger.error(f"Неверный формат даты: {text}")
    raise ValueError("Invalid date format")


__all__ = ["mask_account_card", "get_date"]

__all__ = ["mask_account_card", "get_date", "get_mask_card_number"]  # добавляем alias

# Добавляем псевдоним для совместимости
get_mask_card_number = mask_account_card
