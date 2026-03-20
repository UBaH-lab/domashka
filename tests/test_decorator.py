# -*- coding: utf-8 -*-
"""
Модуль test_decorator содержит тесты для декоратора логирования.

Тестирует функциональность декоратора log() из src.decorators:
- Логирование в консоль
- Логирование в файл
- Обработка исключений
- Корректность формата сообщений

Использует pytest fixtures:
- capsys: для перехвата вывода в консоль
- tmp_path: для создания временных файлов
"""

import pytest

# Импортируем декоратор логирования. Можно импортировать через пакет или напрямую.
# Здесь используем прямой импорт через пакет, как в примерах ранее.
from src.decorators import log


def test_log_to_console_success(capsys):
    """
    Тест: лог в консоль при успешном выполнении функции.

    Проверяет:
    - Наличие строки "my_function started" в выводе
    - Наличие строки "my_function ok" в выводе
    - Наличие строки с результатом функции
    - Корректность возвращаемого значения

    Args:
        capsys: Pytest fixture для захвата stdout/stderr
    """

    @log()  # без filename — лог в консоль
    def my_function(a, b):
        return a + b

    result = my_function(1, 2)
    assert result == 3

    captured = capsys.readouterr()
    assert "my_function started" in captured.out
    assert "my_function ok" in captured.out
    assert "my_function result: 3" in captured.out


def test_log_to_file_success(tmp_path):
    """
    Тест: лог в файл при успешном выполнении функции.

    Проверяет:
    - Создание файла лога
    - Наличие строки "my_function started" в файле
    - Наличие строки "my_function ok" в файле
    - Наличие строки с результатом в файле

    Args:
        tmp_path: Pytest fixture для временной директории
    """
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def my_function(x):
        return x * 2

    result = my_function(5)
    assert result == 10

    content = log_file.read_text(encoding="utf-8")
    assert "my_function started" in content
    assert "my_function ok" in content
    assert "my_function result: 10" in content


def test_log_with_exception(capsys):
    """
    Тест: лог при возникновении исключения.

    Проверяет:
    - Наличие строки "my_function started"
    - Наличие строки "my_function error" с типом исключения
    - Наличие входных параметров в логе ошибки
    - Исключение пробрасывается дальше

    Args:
        capsys: Pytest fixture для захвата stdout/stderr
    """

    @log()
    def my_function(a, b):
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        my_function(1, 2)

    captured = capsys.readouterr()
    assert "my_function started" in captured.out
    assert "my_function error: ValueError" in captured.out
    assert "Inputs:" in captured.out


def test_log_preserves_function_name():
    """
    Тест: декоратор сохраняет имя и docstring функции.

    Проверяет:
    - __name__ обернутой функции совпадает с исходной
    - __doc__ обернутой функции сохраняется

    Использует functools.wraps внутри декоратора.
    """

    @log()
    def my_function():
        """Test docstring."""
        return 42

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "Test docstring."
