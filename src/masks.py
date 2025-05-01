

def get_mask_card_number(card_number:str)->str:
    """ принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован,
    отображается только первые 6 и последние 4 цифры """

    return f"{card_number[:4]}{card_number[4:6]}** ****{card_number[12:]}"



def get_musk_account(account_number: str) -> str:
    """ Принимает на вход номер счёта и возвращает его замаскированный вид.
        Видны только последние 4 цифры номера, аперед ними-две звёздочки ** """

    masked = f"**{account_number[-4:]}"
    return masked

print(get_mask_card_number("7000792289606361"))