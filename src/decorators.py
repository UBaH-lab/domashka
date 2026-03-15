import functools
from typing import Any, Callable, Optional


def log(
    filename: Optional[str] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор логирования:
    - пишет "<func> started" перед вызовом
    - при успехе пишет "<func> ok" и "<func> result: ..."

    - при исключении пишет "<func> error: <ExceptionName>. Inputs: ..."
    Логи либо в указанный файл, либо в консоль (stdout) если filename не задан.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
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

                # Логируем сам результат
                result_line = f"{func.__name__} result: {result!r}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as fh:
                        fh.write(result_line + "\n")
                else:
                    print(result_line)

                return result
            except Exception as exc:
                # Формируем входные параметры для лога ошибки
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
