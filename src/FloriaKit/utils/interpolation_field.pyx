import typing as t
import time

from FloriaKit.utils.calculated_value import CalculatedValue, gcv


T = t.TypeVar('T', default=t.Any)


cdef class _InterpolationField:
    cdef object __weakref__
    cdef object _interpolation_func
    cdef object _delay
    cdef object _value
    cdef object _next  # tuple[next_value, next_time, delay] | None
    cdef bool _is_flash

    def __init__(
        self,
        interpolation_func: t.Callable[[t.Any, t.Any, float], t.Any],
        delay: CalculatedValue[float, []] | float,
        default: t.Any = None,
        flash: bool = False,
    ):
        self._interpolation_func = interpolation_func
        self._delay = delay

        self._value = default
        self._next = None

        self._is_flash = flash

    cpdef object _get_value(self, double now):
        cdef object next_value
        cdef double next_time

        if self._next is None:
            return self._value

        next_value, next_time, delay = self._next

        if now >= next_time:
            self._value = next_value
            self._next = None

            return self._value

        return self._interpolation_func(
            self._value,
            next_value,
            self._get_progress(now),
        )

    cpdef object get_value(self):
        return self._get_value(time.perf_counter())

    cpdef _set_value(self, object value, bool flash):
        cdef double now, delay

        if flash:
            self._next = None
            self._value = value

        else:
            now = time.perf_counter()
            delay = self._get_delay()

            if self._next is not None:
                self._value = self._get_value(now)

            self._next = (
                value,
                now + delay,
                delay
            )
        
    def set_value(self, value: t.Any, **kw: t.Any):
        self._set_value(value, kw.get('flash', self._is_flash))
        return self

    cpdef double _get_progress(self, double now):
        if self._next is None:
            return 1

        cdef double next_time = self._next[1]
        cdef double delay = self._next[2]

        if now > next_time or delay <= 0:
            return 1

        return min(
            1,
            max(
                0,
                1 - (next_time - now) / delay,
            ),
        )


    @property
    def progress(self) -> double:
        return self._get_progress(time.perf_counter())

    cpdef double _get_delay(self):
        return gcv(self._delay)

    @property
    def delay(self):
        return self._get_delay() if self._next is None else self._next[2]

    @property
    def is_interpolated(self):
        return self._next is not None

    @property
    def next_value(self):
        return None if self._next is None else self._next[0]

    @property
    def is_flash(self):
        return self._is_flash

    @is_flash.setter
    def is_flash(self, value: bool):
        self._is_flash = value


class InterpolationField(_InterpolationField, t.Generic[T]): 
    pass