from datetime import datetime
import re


def mask_account_card(info_card: str) -> str:
    """
    Маскирует номер карты или счёт согласно ожиданиям теста.
    Правила:
    - Для обычных карт: сохраняем текст до первой цифры (prefix),
      затем ставим " **** ****" и последние 4 цифры.
      Пример: "Visa Gold 5999414228426353" -> "Visa Gold **** ****6353"
      Пример: "Mastercard Platinum 1234 5678 9876 5432" -> "Mastercard Platinum **** ****5432"
    - Для счетов (начинается с 'Счет'): если в строке есть 16 цифр,
      возвращаем "Счет **<последние 4 цифры>"; иначе "Счет **!".
    """
    if not isinstance(info_card, str) or info_card == "":
        return info_card

    # Определяем префикс перед цифрами: всё до первой цифры
    m = re.match(r"^(.*?)(?=\d)", info_card)
    if not m:
        return info_card
    prefix = m.group(1).strip()

    digits = "".join(ch for ch in info_card if ch.isdigit())
    if not digits:
        return info_card

    if info_card.strip().startswith("Счет"):
        if len(digits) >= 16:
            return f"{prefix} **{digits[-4:]}"
        else:
            return f"{prefix} **!"
    else:
        if len(digits) >= 16:
            return f"{prefix} **** ****{digits[-4:]}"
        else:
            # Для невалидной длины лучше вернуть исходную строку
            return info_card


def get_date(date_inp: str) -> str:
    """
    Преобразование даты в формат DD.MM.YYYY.
    Поддерживает форматы:
      - 2024-03-11
      - 2024-03-11T12:34:56Z (берём первые 10 символов)
      - 2024-03-11T02:26:18.671407
    """
    date_str = date_inp[:10]
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{date.day:02}.{date.month:02}.{date.year}"


def get_mask_card_number(card_number: str) -> str:
    """
    Доп. утилита: маскировка номера карты по более простой схеме.
    Если вход не строка или короче 16 символов — возвращает исходное значение.
    """
    if not isinstance(card_number, str) or len(card_number) < 16:
        return card_number
    return card_number[:6] + "** ****" + card_number[-4:]
