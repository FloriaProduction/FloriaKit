import typing as t
from libc cimport math


cpdef tuple lerp(
    start: t.Iterable[float],
    end: t.Iterable[float],
    float progress,
):
    cdef list[float] result = []
    cdef float x, y 

    for x, y in zip(start, end, strict=True):
        result.append(x + (y - x) * progress)

    return tuple(result)


cdef tuple calculate(
    vector: tuple,
    values: tuple,
    predicate: t.Callable[[float, float], float],
):
    cdef list result = list(vector)
    cdef int i, n = len(result)
    cdef object value
    cdef float v

    for value in values:
        if isinstance(value, t.Sequence):
            if len(value) != n:
                raise ValueError()
            
            for i in range(n):
                result[i] = predicate(result[i], value[i])
        
        elif isinstance(value, float | int):
            for i in range(n):
                result[i] = predicate(result[i], value)

        else:
            raise ValueError()

    return tuple(result)


cdef float predicate_sum(x: float, y: float):
    return x + y
    
cdef float predicate_sub(x: float, y: float):
    return x - y
    
cdef float predicate_mul(x: float, y: float):
    return x * y
    
cdef float predicate_div(x: float, y: float):
    return x / y if y != 0 else 0


def sum(
    vector: tuple[float, ...],
    *values: tuple[float, ...] | float,
) -> tuple[float, ...]:
    return calculate(vector, values, predicate_sum)

def sub(
    vector: tuple[float, ...],
    *values: tuple[float, ...] | float,
) -> tuple[float, ...]:
    return calculate(vector, values, predicate_sub)

def mul(
    vector: tuple[float, ...],
    *values: tuple[float, ...] | float,
) -> tuple[float, ...]:
    return calculate(vector, values, predicate_mul)

def div(
    vector: tuple[float, ...],
    *values: tuple[float, ...] | float,
) -> tuple[float, ...]:
    return calculate(vector, values, predicate_div)


cpdef float distance(vec1: tuple, vec2: tuple):
    cdef int i, n = len(vec1)

    if n != len(vec2):
        raise ValueError()

    cdef float sum = 0
    for i in range(n):
        sum += math.pow(vec1[i] - vec2[i], 2)
    
    return math.sqrt(sum)


cpdef to_vec2(value: t.Iterable[object]):
    return (*value,)[:2]

cpdef tuple to_vec3(value: t.Iterable[object], object z):
    return (*value, z)[:3]

cpdef tuple to_vec4(value: t.Iterable[object], object z, object w):
    return (*value, z, w)[:4]


def round_(value: tuple, *args: t.Any) -> tuple:
    return tuple(round(arg, *args) for arg in value)