import typing as t


def get_key(func: t.Callable[..., t.Any]) -> str:
    return (
        f'{func.__qualname__};{id(func)}'
        if (instance := getattr(func, '__self__', None)) is None
        else f'{func.__qualname__};{id(func)};{instance.__class__.__qualname__};{id(instance)};'
    )


__all__ = [
    'get_key',
]
