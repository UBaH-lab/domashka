
def get_mask_card_number(card_number: str) -> str:
    """
    Принимает номер карты и возвращает её маскированный вид.
    Верховные 6 цифр и последние 4 видны, остальные скрыты символами "*".
    """
    # Проверка, что вход — строка и достаточно длинная
    if not isinstance(card_number, str):
        return ""
    length = len(card_number)
    if length < 16:
        # Для коротких номеров (менее 16 символов), просто маскируем внутренние символы
        return card_number[:6] + '*' * (length - 10) + card_number[-4:] if length > 10 else card_number
    return f"{card_number[:4]}{card_number[4:6]}** ****{card_number[12:]}"


def get_mask_account(account_number: str) -> str:
    """
    Принимает номер счёта и возвращает его маскированный вид.
    Виден только последние 4 цифры, перед ними — две звездочки.
    """
    if not isinstance(account_number, str):
        return ""
    if len(account_number) >= 4:
        return f"**{account_number[-4:]}"
    else:
        # если длина меньше 4 или пустой, возвращаем все символы, или просто маску
        return "**" + account_number