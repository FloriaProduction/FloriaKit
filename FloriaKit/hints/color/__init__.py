import typing as t

from ..common import number

from . import (
    const,
)

type rgb = tuple[number, number, number]
type rgba = tuple[number, number, number, number]

type color = t.Union[
    rgb,
    rgba,
]


def get_rgba(value: color) -> rgba:
    if isinstance(value, tuple):
        r_value = tuple(round(v) for v in value)

        if (l := len(r_value)) == 3:
            return (*r_value, 255)  # pyright: ignore[reportReturnType]

        elif l == 4:
            return (*r_value,)  # pyright: ignore[reportReturnType]

    raise


def get_rgb(value: color) -> rgb:
    if isinstance(value, tuple):
        r_value = tuple(round(v) for v in value)

        if (l := len(r_value)) == 3:
            return (*r_value,)  # pyright: ignore[reportReturnType]

        elif l == 4:
            return (*r_value[:3],)  # pyright: ignore[reportReturnType]

    raise


__all__ = [
    'const',
    #
    'rgb',
    'rgba',
    'color',
    #
    'get_rgba',
    'get_rgb',
]
