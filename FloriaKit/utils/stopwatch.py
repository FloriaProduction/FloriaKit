import typing as t
import types as ts
from contextlib import contextmanager
from time import perf_counter
from collections import deque
import functools
import inspect

if t.TYPE_CHECKING:
    from .. import protocols


class Stopwatch:
    """Таймер для измерения времени выполнения.

    Пример:

    ```python
        stopwatch = Stopwatch(5)

        with stopwatch:
            ...
    ```
    """

    __slots__ = (
        '_start_time',
        '_last_value',
        '_samples',
    )

    def __init__(self, max_samples: int = 10):
        """Инициализация Stopwatch.

        Args:
            max_samples (int, optional): Максимальное количество хранимых замеров. По умолчанию 10.
        """
        self._start_time: float | None = None

        self._last_value: float | None = None
        self._samples: deque[float] = deque(maxlen=max_samples)

    def __enter__(self, *args: t.Any, **kwargs: t.Any):
        self.start()
        return self

    def __exit__(self, *args: t.Any, **kwargs: t.Any):
        self.stop()

    @contextmanager
    def bind(self):
        """Альтернативный способ измерения через контекстный менеджер."""
        try:
            self.start()

            yield self

        finally:
            self.stop()

    def start(self) -> t.Self:
        """Запуск таймера.

        Raises:
            RuntimeError: Если таймер уже запущен.
        """
        if self._start_time is not None:
            raise RuntimeError('Stopwatch is already running')
        self._start_time = perf_counter()

        return self

    def stop(self) -> float:
        """
        Остановка таймера и сохранение результата.

        Returns:
            float: Прошедшее время в секундах.

        Raises:
            RuntimeError: Если таймер не запущен.
        """
        if self._start_time is None:
            raise RuntimeError("Stopwatch is not running")

        self._last_value = perf_counter() - self._start_time
        self._samples.append(self._last_value)

        self._start_time = None
        return self._last_value

    def lap(self) -> float:
        """
        Получить промежуточное время без остановки таймера.

        Returns:
            float: Время с начала измерения.

        Raises:
            RuntimeError: Если таймер не запущен.
        """
        if self._start_time is None:
            raise RuntimeError("Stopwatch is not running")

        return perf_counter() - self._start_time

    def reset(self) -> t.Self:
        """Сброс всех замеров и текущего значения."""
        if self._start_time is not None:
            raise RuntimeError("Stopwatch is running")

        self._samples.clear()
        self._last_value = None

        return self

    @property
    def is_running(self) -> bool:
        """Проверка, запущен ли таймер."""
        return self._start_time is not None

    @property
    def last(self) -> float:
        """Последнее зафиксированное время."""
        if self._last_value is None:
            raise
        return self._last_value

    @property
    def min(self) -> float:
        """Минимальное значение из всех сохранённых замеров."""
        return min(*self._samples) if self.count > 0 else 0

    @property
    def max(self) -> float:
        """Максимальное значение из всех сохранённых замеров."""
        return max(*self._samples) if self.count > 0 else 0

    @property
    def avg(self) -> float:
        """Среднее значение всех сохранённых замеров."""
        if (count := len(self._samples)) > 0:
            return sum(self._samples) / count
        return 0

    @property
    def total(self) -> float:
        """Сумма всех сохранённых замеров."""
        return sum(self._samples)

    @property
    def count(self) -> int:
        """Количество сохранённых замеров."""
        return len(self._samples)

    def __repr__(self) -> str:
        avg = round(self.avg, 6) if self.count > 0 else None
        last = round(self.last, 6) if self._last_value is not None else None
        return f'Stopwatch<{id(self)}>(avg: {avg}(~{None if avg is None else round(1 / avg, 1)}), last: {last}(~{None if last is None else round(1 / last, 1)}))'

    def __str__(self) -> str:
        return self.__repr__()


class _StopwatchDescriptor:
    """Дескриптор для привязки stopwatch к экземплярам классов."""

    def __init__(
        self,
        func: protocols.functions.SyncFunction[...],
        stopwatch: Stopwatch | None = None,
    ):
        self.func = func
        self.stopwatch = stopwatch or Stopwatch()

        functools.update_wrapper(self, func)

    def __get__(self, obj: t.Any, objtype: t.Type[t.Any] | None = None) -> t.Any:
        if obj is None:
            return self

        @functools.wraps(self.func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            with self.stopwatch:
                return self.func(obj, *args, **kwargs)

        wrapper.__stopwatch__ = self.stopwatch  # type: ignore
        return wrapper

    def __call__(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        with self.stopwatch:
            return self.func(*args, **kwargs)


@t.overload
def stopwatch[TFunc: protocols.functions.SyncFunction[...]](
    func: TFunc,
    /,
) -> TFunc: ...


@t.overload
def stopwatch[TFunc: protocols.functions.SyncFunction[...]](
    *,
    instance: Stopwatch | None = None,
) -> t.Callable[[TFunc], TFunc]: ...


def stopwatch(
    func: protocols.functions.SyncFunction[...] | None = None,
    *,
    instance: Stopwatch | None = None,
) -> t.Any:
    """Декоратор для измерения времени выполнения функций и методов.

    Пример:

    ```python
        # Для функции
        @stopwatch
        def my_function():
            ...

    ```

    Пример с общим stopwatch:

    ```python
        shared_sw = Stopwatch()

        @stopwatch(instance=shared_sw)
        def shared_function():
            ...
    ```

    Пример с методом класса:

    ```python
        # Каждый метод имеет свой stopwatch
        class MyClass:
            @stopwatch
            def my_method(self):
                ...
    ```

    """

    def decorator[TFunc: protocols.functions.SyncFunction[...]](func: TFunc) -> TFunc:
        if inspect.ismethod(func) or (
            hasattr(func, '__self__') and getattr(func, '__self__', None) is not None
        ):
            wrapper = _StopwatchDescriptor(func, instance)
            return t.cast(TFunc, wrapper)

        else:
            descriptor = _StopwatchDescriptor(func, instance)
            return t.cast(TFunc, descriptor)

    if func is None:
        return decorator
    else:
        return decorator(func)


__all__ = [
    'Stopwatch',
    'stopwatch',
]
