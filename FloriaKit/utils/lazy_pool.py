import typing as t
from abc import ABC


class BaseLazyPool[**P = [], R = t.Any](ABC):
    __slots__ = ('_queue',)

    def __init__(self) -> None:
        super().__init__()

        self._queue = t.Deque[t.Callable[P, R]]()

    def add(self, func: t.Callable[P, R]) -> t.Self:
        self._queue.append(func)
        return self


class LazyPool[**P = [], R = t.Any](BaseLazyPool[P, R]):
    __slots__ = ()

    def process(self, *args: P.args, **kw: P.kwargs):
        while len(self._queue) > 0:
            self._queue.pop()(*args, **kw)


__all__ = [
    'LazyPool',
]
