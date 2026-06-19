import typing as t

from ..common import number

type rgb = tuple[number, number, number]
type rgba = tuple[number, number, number, number]

type color = t.Union[
    rgb,
    rgba,
]

def get_rgba(value: color) -> rgba: ...
def get_rgb(value: color) -> rgb: ...

__all__ = [
    'rgb',
    'rgba',
    'color',
    #
    'get_rgba',
    'get_rgb',
]
