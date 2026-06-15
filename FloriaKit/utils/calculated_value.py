import typing as t


@t.runtime_checkable
class CalculatedValue[R, **P = []](t.Protocol):
    def __call__(self, *args: P.args, **kwds: P.kwargs) -> R: ...


def gcv[T, **P = []](
    value: CalculatedValue[T, P] | T,
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    if isinstance(value, CalculatedValue):
        return value(*args, **kwargs)  # pyright: ignore[reportUnknownVariableType]
    return value


__all__ = [
    'CalculatedValue',
    'gcv',
]
