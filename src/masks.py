import re
from datetime import datetime

def mask_account_card(text: str) -> str:
    """
    Маскирует текст, содержащий номер карты или счёт.
    Правила:
    - Карты: префикс до первой цифры сохраняется, затем "**** ****" и последние 4 цифры.
      Примеры:
        "Visa Gold 5999414228426353" -> "Visa Gold **** ****6353"
        "Mastercard Platinum 1234 5678 9876 5432" -> "Mastercard Platinum **** ****5432"
        "Мастеркард 1111222233334444" -> "Мастеркард **** ****4444"
    - Счета (начинается с "Счет"): префикс + "**" + последние 4 цифры (или меньше, если нет 4 цифр)
      Примеры:
        "Счет 1234567890123456" -> "Счет **3456"
        "Счет 123" -> "Счет **123"
        "Счет 9876543210" -> "Счет **3210"
    - Если цифр в строке нет, возвращаем исходную строку.
    """
    if not isinstance(text, str) or text == "":
        return text

    m = re.search(r"\d", text)
    if not m:
        return text  # нет цифр

    prefix_with_space = text[:m.start()]  # может включать пробел после префикса

    digits_only = re.sub(r"\D", "", text[m.start():])
    if not digits_only:
        return text

    last = digits_only[-4:] if len(digits_only) >= 4 else digits_only

    if text.strip().startswith("Счет"):
        return prefix_with_space + "**" + last

    return prefix_with_space + "**** ****" + last


def get_date(text: str) -> str:
    """
    Преобразует дату в формате ISO-like в строку DD.MM.YYYY.
    Поддерживает:
      - 2024-03-11T02:26:18.671407
      - 2020-01-01T00:00:00.000000
      - 2022-12-31T23:59:59
      - 2024-07-15
    При неверном формате возбуждает ValueError.
    """
    if not isinstance(text, str):
        raise ValueError("Date must be a string")

    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            continue

    raise ValueError("Invalid date format")