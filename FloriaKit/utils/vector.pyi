import typing as t

from .. import hints
from ..hints import number

# lerp
def lerp[
    T: hints.vec2[number] | hints.vec3[number] | hints.vec4[number] | tuple[number, ...]
](
    start: T,
    end: T,
    progress: number,
) -> T: ...

# sum
@t.overload
def sum[T: hints.vec2[number]](
    vector: T,
    *values: hints.vec2[number] | number,
) -> T: ...
@t.overload
def sum[T: hints.vec3](
    vector: T,
    *values: hints.vec3 | number,
) -> T: ...
@t.overload
def sum[T: hints.vec4](
    vector: T,
    *values: hints.vec4 | number,
) -> T: ...
@t.overload
def sum(
    vector: tuple[number, ...],
    *values: tuple[number, ...] | number,
) -> tuple[number, ...]: ...

# sub
@t.overload
def sub[T: hints.vec2[number]](
    vector: T,
    *values: hints.vec2[number] | number,
) -> T: ...
@t.overload
def sub[T: hints.vec3](
    vector: T,
    *values: hints.vec3 | number,
) -> T: ...
@t.overload
def sub[T: hints.vec4](
    vector: T,
    *values: hints.vec4 | number,
) -> T: ...
@t.overload
def sub(
    vector: tuple[number, ...],
    *values: tuple[number, ...] | number,
) -> tuple[number, ...]: ...

# mul
@t.overload
def mul[T: hints.vec2[number]](
    vector: T,
    *values: hints.vec2[number] | number,
) -> T: ...
@t.overload
def mul[T: hints.vec3](
    vector: T,
    *values: hints.vec3 | number,
) -> T: ...
@t.overload
def mul[T: hints.vec4](
    vector: T,
    *values: hints.vec4 | number,
) -> T: ...
@t.overload
def mul(
    vector: tuple[number, ...],
    *values: tuple[number, ...] | number,
) -> tuple[number, ...]: ...

# div
@t.overload
def div[T: hints.vec2[number]](
    vector: T,
    *values: hints.vec2[number] | number,
) -> T: ...
@t.overload
def div[T: hints.vec3](
    vector: T,
    *values: hints.vec3 | number,
) -> T: ...
@t.overload
def div[T: hints.vec4](
    vector: T,
    *values: hints.vec4 | number,
) -> T: ...
@t.overload
def div(
    vector: tuple[number, ...],
    *values: tuple[number, ...] | number,
) -> tuple[number, ...]: ...

# distance
def distance[
    T: hints.vec2[number] | hints.vec3[number] | hints.vec4[number] | tuple[number, ...]
](
    vec1: T,
    vec2: T,
) -> number: ...

# to_vecX
def to_vec2[T](value: t.Iterable[T]) -> hints.vec2[T]: ...
def to_vec3[T](value: t.Iterable[T], z: T) -> hints.vec3[T]: ...
def to_vec4[T](value: t.Iterable[T], z: T, w: T) -> hints.vec4[T]: ...

# round_
@t.overload
def round_(value: hints.vec2[number], /) -> hints.vec2i: ...
@t.overload
def round_(value: hints.vec3[number], /) -> hints.vec3i: ...
@t.overload
def round_(value: hints.vec4[number], /) -> hints.vec4i: ...
@t.overload
def round_(value: tuple[number, ...], /) -> tuple[int, ...]: ...
@t.overload
def round_[
    T: hints.vec2[number] | hints.vec3[number] | hints.vec4[number] | tuple[number, ...]
](
    value: T,
    ndigits: int,
    /,
) -> T: ...
