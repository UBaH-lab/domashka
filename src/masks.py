

def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты по шаблону:
    - Для номеров >= 16 символов: 'XXXXXX** ****XXXX'
    - Для номеров длиной от 11 до 15 символов: 'XXXXXX** ****XXXX'
    - Для коротких — возвращает как есть.
    """
    if not isinstance(card_number, str):
        return ""
    length = len(card_number)
    if length >= 16:
        return f"{card_number[:6]}** ****{card_number[12:]}"
    elif length > 10:
        return f"{card_number[:6]}** ****{card_number[-4:]}"
    else:
        return card_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта, показывая только последние 4 цифры,
    перед ними — две звездочки.
    """
    if not isinstance(account_number, str):
        return ""
    if len(account_number) >= 4:
        return f"**{account_number[-4:]}"
    else:
        return "**" + account_number  # на случай очень коротких номеров
