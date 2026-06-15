import contextlib
import typing as t


@contextlib.contextmanager
def empty[TD: t.Any | None](
    default: TD = None,
) -> t.Generator[TD, t.Any, None]:
    yield default


@contextlib.asynccontextmanager
async def empty_async[TD: t.Any | None](
    default: TD = None,
) -> t.AsyncGenerator[TD, t.Any]:
    yield default


__all__ = [
    'empty',
    'empty_async',
]
