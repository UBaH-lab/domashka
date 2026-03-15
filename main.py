"""Модуль для тестирования маскирования номера карты."""

import logging

from src.masks import get_mask_card_number

# Настройка логирования с записью в файл
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="logs/app.log",
    encoding="utf-8",
)


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
