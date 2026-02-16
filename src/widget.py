from masks import get_mask_card_number
from datetime import datetime


def mask_account_card(info_card: str) -> str:
    """Функция определяет счет это или номер карты и возвращает замаскированную строку."""
    info_card_list = info_card.split()
    if "Счет" in info_card_list:
        # Возвращаем строку с частью номер счета
        return f"Счет **{info_card_list[-1][-4:]}"
    else:
        card_name = ' '.join(info_card_list[:-1])
        card_number = info_card_list[-1].replace(' ', '')
        return f"{card_name} {get_mask_card_number(card_number)}"


card_type_and_number = "Visa Gold 5999414228426353"
mask_account_card(card_type_and_number)


def get_date(date_inp: str) -> str:
    """Функция, которая принимает на вход строку и возвращает строку с датой."""
    date = datetime.strptime(date_inp[:10], '%Y-%m-%d')
    return f"{date.day:02}.{date.month:02}.{date.year}"


print(get_date("2024-03-11T02:26:18.671407"))
