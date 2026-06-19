import typing as t

from ..common import number


rgb = tuple[number, number, number]
rgba = tuple[number, number, number, number]

color = t.Union[
    rgb,
    rgba,
]


cpdef tuple[int, int, int, int] get_rgba(value: object):
    cdef object v
    cdef list[int] result = []

    if isinstance(value, tuple):
        for v in value:
            result.append(round(v))

        if len(result) == 3:
            result.append(255)

    if result:
        return tuple(result)

    raise


cpdef tuple[int, int, int] get_rgb(value: object):
    cdef object v
    cdef list[int] result = []

    if isinstance(value, tuple):
        for v in value:
            result.append(round(v))

        if len(result) == 4:
            result = result[:3]

    if result:
        return tuple(result)

    raise

