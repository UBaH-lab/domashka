from datetime import datetime


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя первые 6 и последние 4 символа видимыми, остальное заменяет звездочками."""
    if not isinstance(card_number, str) or len(card_number) < 16:
        return card_number  # Если номер слишком короткий или не строка — возвращаем как есть

    # Первый блок 6 символов, потом две группы по 2 символа заменяем на **
    return card_number[:6] + "** ****" + card_number[-4:]


def mask_account_card(info_card: str) -> str:
    """
    Функция определяет счет это или номер карты и возвращает замаскированную строку.
    Если 'Счет' в строке — маскирует счет, иначе номер карты.
    """
    info_card_list = info_card.split()
    if "Счет" in info_card_list:
        # Возвращаем строку с частью номера счета
        return f"Счет **{info_card_list[-1][-4:]}"
    else:
        card_name = " ".join(info_card_list[:-1])
        card_number = info_card_list[-1].replace(" ", "")
        return f"{card_name} {get_mask_card_number(card_number)}"


def get_date(date_inp: str) -> str:
    """
    Функция, которая принимает на вход строку и возвращает строку с датой в формате ДД.ММ.ГГГГ.
    """
    date = datetime.strptime(date_inp[:10], "%Y-%m-%d")
    return f"{date.day:02}.{date.month:02}.{date.year}"


# Пример использования
if __name__ == "__main__":
    card_type_and_number = "Visa Gold 5999414228426353"
    print(mask_account_card(card_type_and_number))

    print(get_date("2024-03-11T02:26:18.671407"))
