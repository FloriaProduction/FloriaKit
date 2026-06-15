import typing as t


class SyncFunction[**P = [], R = t.Any](t.Protocol):
    def __call__(self, *args: P.args, **kwds: P.kwargs) -> R: ...


class AsyncFunction[**P = [], R = t.Any](t.Protocol):
    async def __call__(self, *args: P.args, **kwds: P.kwargs) -> R: ...


type AnyFunction[**P = [], R = t.Any] = t.Union[
    SyncFunction[P, R],
    AsyncFunction[P, R],
]

__all__ = [
    'SyncFunction',
    'AsyncFunction',
    'AnyFunction',
]
