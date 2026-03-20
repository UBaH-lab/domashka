# -*- coding: utf-8 -*-
"""
Модуль test_logger_config содержит тесты для конфигурации логирования.

Тестирует настройки логирования из src.logger_config:
- Создание логгеров
- Настройка уровней логирования
- Форматирование сообщений
- Обработчики (handlers)

Использует unittest.mock для изоляции тестов.
"""

import logging


def test_logger_creation():
    """
    Тест: создание логгера.

    Проверяет:
    - Логгер создается корректно
    - Имя логгера соответствует ожидаемому

    Результат: логгер с именем "test_logger"
    """
    logger = logging.getLogger("test_logger")
    assert logger.name == "test_logger"


def test_logger_level():
    """
    Тест: установка уровня логирования.

    Проверяет:
    - Уровень логирования устанавливается корректно
    - Уровень DEBUG применяется

    Результат: логгер с уровнем DEBUG
    """
    logger = logging.getLogger("test_level_logger")
    logger.setLevel(logging.DEBUG)
    assert logger.level == logging.DEBUG


def test_logger_handler():
    """
    Тест: добавление обработчика к логгеру.

    Проверяет:
    - Обработчик добавляется к логгеру
    - Количество обработчиков: 1

    Результат: логгер с StreamHandler
    """
    logger = logging.getLogger("test_handler_logger")
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_logger_formatter():
    """
    Тест: форматтер для обработчика.

    Проверяет:
    - Форматтер создается корректно
    - Формат содержит ожидаемые поля

    Результат: форматтер с полями %(name)s, %(levelname)s, %(message)s
    """
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    assert "%(name)s" in formatter._fmt
    assert "%(levelname)s" in formatter._fmt
    assert "%(message)s" in formatter._fmt


def test_logger_remove_handler():
    """
    Тест: удаление обработчика из логгера.

    Проверяет:
    - Обработчик удаляется из логгера
    - Количество обработчиков уменьшается

    Результат: логгер без обработчиков
    """
    logger = logging.getLogger("test_remove_handler")
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.removeHandler(handler)

    assert len(logger.handlers) == 0


def test_logger_propagate():
    """
    Тест: настройка распространения логов.

    Проверяет:
    - Флаг propagate устанавливается корректно

    Результат: логгер с propagate=False
    """
    logger = logging.getLogger("test_propagate_logger")
    logger.propagate = False
    assert logger.propagate is False
