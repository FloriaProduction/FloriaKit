import typing as t

class Flag:
    __slots__ = ('_depth',)

    """
    Управляемый флаг с поддержкой контекстного менеджера.

    Предоставляет механизм временного установления флага с
    автоматическим сбросом при выходе из контекста.

    Пример:

    ```python

        flag = Flag()

        ...

        with flag:
            # Флаг установлен в True
            ...

        # Флаг автоматически сброшен в False

        ...

        if flag:
            raise Exception(...)
    ```
    """

    def __init__(self) -> None: ...
    def __enter__(self, *args: t.Any, **kwargs: t.Any) -> None: ...
    def __exit__(self, *args: t.Any, **kwargs: t.Any) -> None: ...
    @property
    def value(self) -> bool: ...
    def __bool__(self) -> bool: ...

__all__ = ['Flag']
