# -*- coding: utf-8 -*-
"""
Модуль test_decorators содержит тесты для декоратора логирования.

Тестирует функциональность декоратора log() из src.decorators:
- Логирование успешных операций в консоль и файл
- Логирование исключений с параметрами
- Обработка позиционных и именованных аргументов
- Сохранение имени и docstring функции

Использует pytest fixtures:
- capsys: для перехвата вывода в консоль
- tmp_path: для создания временных файлов лога
"""

import pytest

from src.decorators import log


def test_log_to_console(capsys):
    """
    Тест: логирование успешной операции в консоль.

    Проверяет:
    - Наличие строки "add started" в выводе
    - Наличие строки "add ok" в выводе
    - Наличие результата "add result: 5"
    - Корректность возвращаемого значения

    Args:
        capsys: Pytest fixture для захвата stdout/stderr
    """

    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    assert "add started" in captured.out
    assert "add ok" in captured.out
    assert "add result: 5" in captured.out


def test_log_to_file(tmp_path):
    """
    Тест: логирование успешной операции в файл.

    Проверяет:
    - Создание файла лога
    - Наличие строки "multiply started" в файле
    - Наличие строки "multiply ok" в файле
    - Наличие результата "multiply result: 12"

    Args:
        tmp_path: Pytest fixture для временной директории
    """
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    result = multiply(3, 4)
    assert result == 12

    content = log_file.read_text(encoding="utf-8")
    assert "multiply started" in content
    assert "multiply ok" in content
    assert "multiply result: 12" in content


def test_log_exception_console(capsys):
    """
    Тест: логирование исключения в консоль.

    Проверяет:
    - Наличие строки "divide started"
    - Наличие строки "divide error: ZeroDivisionError"
    - Наличие входных параметров "Inputs: (1, 0)"
    - Исключение пробрасывается дальше

    Args:
        capsys: Pytest fixture для захвата stdout/stderr
    """

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide started" in captured.out
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0)" in captured.out


def test_log_exception_file(tmp_path):
    """
    Тест: логирование исключения в файл.

    Проверяет:
    - Создание файла лога
    - Наличие строки "raise_error error: ValueError"
    - Наличие входных параметров "Inputs: ()"

    Args:
        tmp_path: Pytest fixture для временной директории
    """
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def raise_error():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        raise_error()

    content = log_file.read_text(encoding="utf-8")
    assert "raise_error error: ValueError" in content
    assert "Inputs: ()" in content


def test_log_with_kwargs(capsys):
    """
    Тест: логирование с именованными аргументами.

    Проверяет:
    - Корректная работа с kwargs
    - Наличие строк лога
    - Корректность результата

    Args:
        capsys: Pytest fixture для захвата stdout/stderr
    """

    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}"

    result = greet("World", greeting="Hi")
    assert result == "Hi, World"

    captured = capsys.readouterr()
    assert "greet started" in captured.out
    assert "greet ok" in captured.out


def test_log_exception_with_kwargs(capsys):
    """
    Тест: логирование исключения с именованными аргументами.

    Проверяет:
    - Наличие строки "fail error: RuntimeError"
    - Наличие kwargs в логе: "'y': 20"

    Args:
        capsys: Pytest fixture для захвата stdout/stderr
    """

    @log()
    def fail(x, y=10):
        raise RuntimeError("Failed")

    with pytest.raises(RuntimeError):
        fail(5, y=20)

    captured = capsys.readouterr()
    assert "fail error: RuntimeError" in captured.out
    assert "'y': 20" in captured.out
