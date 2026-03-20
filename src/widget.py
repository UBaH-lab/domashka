"""
Модуль widget содержит функции для маскирования данных и форматирования дат.

Эти функции используются для отображения чувствительных данных
(номера карт, счета) в безопасном виде для пользователя.

Маскирование — это скрытие части информации символами *,
чтобы защитить данные, но оставить их узнаваемыми.
"""

from datetime import datetime
import re


def mask_account_card(info_card: str) -> str:
    """
    Маскирует номер карты или счёта для безопасного отображения.

    Правила маскирования:
    - Для карт: сохраняет префикс (название карты), затем маска и последние 4 цифры
      "Visa Gold 5999414228426353" -> "Visa Gold **** ****6353"
    - Для счетов (начинается с "Счет"): маска короче
      "Счет 12345678901234567890" -> "Счет **7890"

    Args:
        info_card (str): Строка с названием и номером карты или счёта.
            Формат: "Название_карты номер" или "Счет номер"

    Returns:
        str: Маскированная строка.
            - Для карт: "Префикс **** ****XXXX" (где XXXX — последние 4 цифры)
            - Для счетов: "Префикс **XXXX"
            - Для некорректных данных: возвращает как есть

    Examples:
        >>> mask_account_card("Visa Gold 5999414228426353")
        'Visa Gold **** ****6353'

        >>> mask_account_card("Mastercard 1234567890123456")
        'Mastercard **** ****3456'

        >>> mask_account_card("Счет 12345678901234567890")
        'Счет **7890'

        >>> mask_account_card("")
        ''

        >>> mask_account_card(None)
        None

    Note:
        - Если номер короче 16 цифр, возвращается исходная строка
        - Для счетов с коротким номером добавляется "!"
        - Пустая строка и None возвращаются без изменений
    """
    if not isinstance(info_card, str) or info_card == "":
        return info_card

    # Определяем префикс перед цифрами: всё до первой цифры
    m = re.match(r"^(.*?)(?=\d)", info_card)
    if not m:
        return info_card
    prefix = m.group(1).strip()

    # Извлекаем все цифры из строки
    digits = "".join(ch for ch in info_card if ch.isdigit())

    if info_card.strip().startswith("Счет"):
        # Для счетов: маска короче
        if len(digits) >= 4:
            return f"{prefix} **{digits[-4:]}"
        elif len(digits) > 0:
            return f"{prefix} **{digits}"
        else:
            return f"{prefix} **!"
    else:
        # Для карт: стандартная маска
        if len(digits) >= 16:
            return f"{prefix} **** ****{digits[-4:]}"
        else:
            # Для невалидной длины возвращаем исходную строку
            return info_card


def get_date(date_inp: str) -> str:
    """
    Преобразует дату из ISO-формата в читаемый вид DD.MM.YYYY.

    Поддерживает различные форматы ISO:
    - "2024-03-11" -> "11.03.2024"
    - "2024-03-11T12:34:56Z" -> "11.03.2024"
    - "2024-03-11T02:26:18.671407" -> "11.03.2024"

    Args:
        date_inp (str): Строка с датой в ISO-формате.
            Берутся первые 10 символов (YYYY-MM-DD).

    Returns:
        str: Дата в формате DD.MM.YYYY.

    Raises:
        ValueError: Если строка не является корректной датой.

    Examples:
        >>> get_date("2024-03-11")
        '11.03.2024'

        >>> get_date("2024-03-11T12:34:56Z")
        '11.03.2024'

        >>> get_date("2024-12-01")
        '01.12.2024'

    Note:
        Время (часы, минуты, секунды) игнорируется.
        Используются только год, месяц и день.
    """
    date_str = date_inp[:10]  # Берем только дату без времени
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{date.day:02}.{date.month:02}.{date.year}"


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты по упрощенной схеме.

    Показывает первые 6 цифр (BIN карты) и последние 4 цифры,
    остальные заменяются на звёздочки.

    Args:
        card_number (str): Номер карты (16 цифр, без пробелов).

    Returns:
        str: Маскированный номер в формате "XXXXXX** ****XXXX".
            Если вход некорректен, возвращается без изменений.

    Examples:
        >>> get_mask_card_number("1234567890123456")
        '123456** ****3456'

        >>> get_mask_card_number("12345")
        '12345'

        >>> get_mask_card_number(None)
        None

    Note:
        Первые 6 цифр — это BIN (Bank Identification Number),
        который идентифицирует банк и тип карты.
    """
    if not isinstance(card_number, str) or len(card_number) < 16:
        return card_number
    return card_number[:6] + "** ****" + card_number[-4:]
