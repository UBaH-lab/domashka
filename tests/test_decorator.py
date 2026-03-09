import pytest

# Импортируем декоратор логирования. Можно импортировать через пакет или напрямую.
# Здесь используем прямой импорт через пакет, как в примерах ранее.
from src.decorators import log


def test_log_to_console_success(capsys):
    """
    Тест: лог в консоль при успешном выполнении функции.
    Проверяем наличие строк "my_function started" и "my_function ok".
    """

    @log()  # без filename — лог в консоль
    def my_function(a, b):
        return a + b

    assert my_function(1, 2) == 3

    captured = capsys.readouterr()
    assert "my_function started" in captured.out
    assert "my_function ok" in captured.out


def test_log_to_file_success(tmp_path):
    """
    Тест: лог в файл при успешном выполнении функции.
    Проверяем наличие строк "my_function started" и "my_function ok" в файле.
    """
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def my_function(a, b):
        return a + b

    assert my_function(1, 2) == 3

    content = log_file.read_text(encoding="utf-8")
    assert "my_function started" in content
    assert "my_function ok" in content


def test_log_to_file_error(tmp_path):
    """
    Тест: лог ошибки в файл, включая Inputs: (...).
    """

    log_file = tmp_path / "log_err.txt"

    @log(filename=str(log_file))
    def bad(a, b):
        raise ValueError("boom")

    with pytest.raises(ValueError):
        bad(1, 2)

    content = log_file.read_text(encoding="utf-8")
    # Проверяем наличие части строки об ошибке и входных параметрах
    assert "bad error: ValueError" in content
    assert "Inputs: (1, 2)" in content


def test_log_to_console_error(capsys):
    """
    Тест: лог ошибки в консоль, включая Inputs: (...).
    """

    @log()  # без filename — лог в консоль
    def bad(a, b):
        raise ValueError("boom")

    with pytest.raises(ValueError):
        bad(1, 2)

    captured = capsys.readouterr()
    assert "bad error: ValueError" in captured.out
    assert "Inputs: (1, 2)" in captured.out
