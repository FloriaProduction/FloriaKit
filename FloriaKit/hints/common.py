import typing as t
import pathlib

type number = int | float

# vec2

type vec2[T = number] = tuple[T, T]
type pos2[T = number] = vec2[T]
type size2[T = number] = vec2[T]
type scale2[T = number] = vec2[T]

type vec2i = vec2[int]
type pos2i = vec2i
type size2i = vec2i
type scale2i = vec2i

# vec3

type vec3[T = number] = tuple[T, T, T]
type pos3[T = number] = vec3[T]
type size3[T = number] = vec3[T]
type scale3[T = number] = vec3[T]

type vec3i = vec3[int]
type pos3i = vec3i
type size3i = vec3i
type scale3i = vec3i

# vec4

type vec4[T = number] = tuple[T, T, T, T]
type vec4i = vec4[int]

# other

type OneOrMany[T] = t.Iterable[T] | T


type orientation = t.Literal[
    'vertical',
    'horizontal',
]

type PathOrStr = pathlib.Path | str


def get_path(value: PathOrStr) -> pathlib.Path:
    if isinstance(value, str):
        return pathlib.Path(value)
    return value


__all__ = [
    'number',
    #
    'vec2',
    'pos2',
    'size2',
    'scale2',
    'vec2i',
    'pos2i',
    'size2i',
    'scale2i',
    #
    'vec3',
    'pos3',
    'size3',
    'scale3',
    'vec3i',
    'pos3i',
    'size3i',
    'scale3i',
    #
    'vec4',
    'vec4i',
    #
    'OneOrMany',
    'orientation',
    'PathOrStr',
    'get_path',
]
