import typing as t

from .common import number, vec2

type AlignSimple = t.Literal[
    'lt',
    't',
    'rt',
    'r',
    'rb',
    'b',
    'lb',
    'l',
    'c',
]

class _AlignLeft(t.TypedDict, total=False):
    left: number

class _AlignCenterX(t.TypedDict, total=False):
    center_x: number

class _AlignRight(t.TypedDict, total=False):
    right: number

class _AlignTop(t.TypedDict, total=False):
    top: number

class _AlignCenterY(t.TypedDict, total=False):
    center_y: number

class _AlignBottom(t.TypedDict, total=False):
    bottom: number

class _AlignLeftTop(_AlignLeft, _AlignTop): ...
class _AlignLeftCenterY(_AlignLeft, _AlignCenterY): ...
class _AlignLeftBottom(_AlignLeft, _AlignBottom): ...
class _AlignCenterXTop(_AlignCenterX, _AlignTop): ...
class _AlignCenterXCenterY(_AlignCenterX, _AlignCenterY): ...
class _AlignCenterXBottom(_AlignCenterX, _AlignBottom): ...
class _AlignRightTop(_AlignRight, _AlignTop): ...
class _AlignRightCenterY(_AlignRight, _AlignCenterY): ...
class _AlignRightBottom(_AlignRight, _AlignBottom): ...

type AlignDetail = t.Union[
    _AlignLeftTop,
    _AlignLeftCenterY,
    _AlignLeftBottom,
    _AlignCenterXTop,
    _AlignCenterXCenterY,
    _AlignCenterXBottom,
    _AlignRightTop,
    _AlignRightCenterY,
    _AlignRightBottom,
]

type AlignAny = t.Union[
    AlignSimple,
    AlignDetail,
]

def calculate_align(size: vec2, align: AlignAny) -> vec2: ...

__all__ = [
    'AlignSimple',
    'AlignDetail',
    'AlignAny',
    'calculate_align',
]
