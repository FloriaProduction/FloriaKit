import typing as t
import asyncio
import contextlib

from .. import hints

from .calculated_value import CalculatedValue, gcv

if t.TYPE_CHECKING:

    @t.overload
    def coalapse[T](
        *items: T | None,
        exception: hints.ExceptionOrStr | None = None,
    ) -> T: ...

    @t.overload
    def coalapse[T, TD](
        *items: T | None,
        default: TD,
    ) -> T | TD: ...


def coalapse(
    *items: t.Any | None,
    **kw: t.Any,
) -> t.Any:
    for item in items:
        if item is not None:
            return item

    if 'default' in kw:
        return kw['default']

    raise hints.get_exception(
        kw.get('exception'),
        default=ValueError(),
    )


if t.TYPE_CHECKING:

    @t.overload
    def coalapse_lazy[T](
        *items: CalculatedValue[T | None] | T | None,
        exception: hints.ExceptionOrStr | None = None,
    ) -> T: ...

    @t.overload
    def coalapse_lazy[T, TD](
        *items: CalculatedValue[T | None] | T | None,
        default: TD,
    ) -> T | TD: ...


def coalapse_lazy(
    *items: CalculatedValue[t.Any] | t.Any | None,
    **kw: t.Any,
) -> t.Any:
    for item in items:
        if (value := gcv(item)) is not None:
            return value

    if 'default' in kw:
        return kw['default']

    raise hints.get_exception(
        kw.get('exception'),
        default=ValueError(),
    )


async def invoke[**P, R](
    func: t.Callable[P, R | t.Coroutine[R, t.Any, t.Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    if asyncio.iscoroutine(result := func(*args, **kwargs)):
        return await result
    return result


def partition[T](
    predicate: t.Callable[[T], bool] | None,
    iterable: t.Iterable[T],
) -> tuple[list[T], list[T]]:
    '''
    return: trues, falses
    '''

    trues: list[T] = []
    falses: list[T] = []

    for item in iterable:
        if item is not None if predicate is None else predicate(item):
            trues.append(item)
        else:
            falses.append(item)

    return trues, falses


def ensure_iterable[T](value: T | t.Iterable[T]) -> t.Iterable[T]:
    if isinstance(value, t.Iterable) and not isinstance(value, (str, bytes, bytearray)):
        return value  # pyright: ignore[reportUnknownVariableType]
    else:
        return [value]  # pyright: ignore[reportReturnType]


async def yield_every[T: t.Any](
    items: t.Iterable[T],
    *,
    step: int = 100,
    pause: float = 0,
    progress_callback: (
        t.Callable[[int, T], t.Coroutine[t.Any, t.Any, t.Any] | t.Any] | None
    ) = None,
) -> t.AsyncIterable[T]:
    """
    Асинхронно перебирает элементы с периодическими паузами для кооперативной многозадачности.

    Эта функция позволяет обрабатывать большие коллекции данных, периодически
    отдавая управление другим асинхронным задачам, что предотвращает блокировку
    event_loop и улучшает отзывчивость приложения.

    Args:
        items: Итерируемая коллекция элементов для обработки
        step: Количество элементов между паузами.
        pause: Длительность паузы в секундах. Может быть 0 для минимального переключения контекста.
        progress_callback: Функция, вызываемая для каждого элемента с его индексом.

    Yields:
        T: Очередной элемент из коллекции.

    Raises:
        ValueError: Если `step` отрицательное или ровно нулю.

    Example:

    ```python
        # Базовое использование
        async for item in yield_every(range(100), step=10):
            process(item)

        # С обработкой прогресса
        async for item in yield_every(data, progress_callback=lambda i, x: print(f"Обработано: {i / len(data)}%")):
            await process_async(item)
    ```
    """

    if step <= 0:
        raise ValueError(f"Step must be non-negative, got {step}")

    for i, item in enumerate(items):
        yield item

        if progress_callback is not None:
            await invoke(progress_callback, i, item)

        if step > 0 and i % step == 0:
            await asyncio.sleep(pause)


@contextlib.contextmanager
def try_import(exception: hints.ExceptionOrStr | None = None):
    try:
        yield

    except ImportError as ex:
        if exception is None:
            raise

        raise hints.get_exception(exception) from ex
