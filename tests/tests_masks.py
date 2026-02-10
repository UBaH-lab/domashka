
import masks

def test_get_mask_card_number():
    # Граничные и стандартные случаи
    # Стандартный номер (длина 16)
    assert masks.get_mask_card_number("7000792289606361") == "700079** ****6361"

    # Менее 16 символов, например 10
    assert masks.get_mask_card_number("1234567890") == "1234567890"  # по коду, так как длиннее 10
    # Менее 16, при этом длина 14
    assert masks.get_mask_card_number("12345678901234") == "123456** ****1234"
    # Очень короткий номер
    assert masks.get_mask_card_number("12345") == "12345"  # просто возвращает как есть

    # Не строка
    assert masks.get_mask_card_number(None) == ""
    assert masks.get_mask_card_number(1234567890) == ""

def test_get_mask_account():
    # стандартный номер
    assert masks.get_mask_account("1234567890") == "**7890"

    # Короче 4 символов
    assert masks.get_mask_account("123") == "**123"
    assert masks.get_mask_account("") == "**"

    # Не строка
    assert masks.get_mask_account(None) == ""
    assert masks.get_mask_account(12345) == ""

# Запуск тестов при запуске файла
if __name__ == "__main__":
    test_get_mask_card_number()
    test_get_mask_account()
    print("Все тесты прошли успешно!")