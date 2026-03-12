"""
Модуль для настройки конфигурации логирования в проекте.

Создает и настраивает логеры для записи в файлы в папке logs.
Логи перезаписываются при каждом запуске приложения.
"""

import logging
from pathlib import Path


def setup_logger(module_name: str) -> logging.Logger:
    """
    Создает и настраивает логер для указанного модуля.

    Параметры:
    - module_name: имя модуля (например, 'masks', 'utils')

    Возвращает:
    - настроенный экземпляр logging.Logger

    Логи записываются в файл logs/{module_name}.log с форматом:
    {время} - {имя модуля} - {уровень} - {сообщение}
    """
    # Создаем папку logs, если её нет
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Создаем логер
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Очищаем существующие обработчики, чтобы избежать дублирования
    logger.handlers.clear()

    # Создаем файловый обработчик (перезапись при каждом запуске - mode='w')
    log_file = logs_dir / f"{module_name}.log"
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Создаем форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логеру
    logger.addHandler(file_handler)

    return logger
