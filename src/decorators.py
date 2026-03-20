"""
Модуль decorators содержит декоратор для логирования функций.

Декоратор log() позволяет автоматически записывать:
- начало выполнения функции
- успешный результат
- ошибки с входными параметрами

Это полезно для отладки и мониторинга работы программы.
"""

import functools
from typing import Any, Callable, Optional


def log(
    filename: Optional[str] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования вызовов функции.

    Автоматически записывает информацию о работе функции:
    1. "<func> started" — перед началом выполнения
    2. "<func> ok" — при успешном завершении
    3. "<func> result: ..." — результат функции
    4. "<func> error: <Exception>. Inputs: ..." — при ошибке

    Args:
        filename (Optional[str]): Путь к файлу для записи логов.
            Если None, логи выводятся в консоль (stdout).

    Returns:
        Callable: Декоратор, который можно применить к функции.

    Examples:
        >>> @log()
        ... def add(a, b):
        ...     return a + b
        >>> add(1, 2)
        add started
        add ok
        add result: 3
        3

        >>> @log(filename="app.log")
        ... def process():
        ...     return "done"
        >>> process()  # Запишет в файл app.log

    Note:
        При возникновении исключения, ошибка логируется,
        а затем исключение пробрасывается дальше.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Внутренний декоратор, который оборачивает функцию.

        Args:
            func: Функция, которую нужно обернуть.

        Returns:
            Callable: Обернутая функция с логированием.
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Обертка функции с добавлением логирования.

            Args:
                *args: Позиционные аргументы функции.
                **kwargs: Именованные аргументы функции.

            Returns:
                Any: Результат выполнения функции.

            Raises:
                Exception: Пробрасывает все исключения функции.
            """
            # Логируем начало выполнения функции
            start_line = f"{func.__name__} started"
            if filename:
                with open(filename, "a", encoding="utf-8") as fh:
                    fh.write(start_line + "\n")
            else:
                print(start_line)

            try:
                # Вызываем исходную функцию
                result = func(*args, **kwargs)

                # Логируем успешное завершение
                ok_line = f"{func.__name__} ok"
                if filename:
                    with open(filename, "a", encoding="utf-8") as fh:
                        fh.write(ok_line + "\n")
                else:
                    print(ok_line)

                # Логируем результат
                result_line = f"{func.__name__} result: {result!r}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as fh:
                        fh.write(result_line + "\n")
                else:
                    print(result_line)

                return result
            except Exception as exc:
                # Формируем строку с входными параметрами
                inputs_repr = f"{args}, {kwargs}" if kwargs else f"{args}"
                err_line = f"{func.__name__} error: {exc.__class__.__name__}. Inputs: {inputs_repr}"

                # Логируем ошибку
                if filename:
                    with open(filename, "a", encoding="utf-8") as fh:
                        fh.write(err_line + "\n")
                else:
                    print(err_line)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator
