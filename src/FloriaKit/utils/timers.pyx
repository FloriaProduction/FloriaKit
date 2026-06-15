import typing as t
from time import perf_counter
from abc import ABC
import math

from FloriaKit.utils.calculated_value import CalculatedValue, gcv


cdef class VariableTimer:
    cdef object __weakref__
    cdef object _interval
    cdef double _next_time, _last_time

    def __init__(self, interval: CalculatedValue[double, []] | double = 0):
        self._interval = interval
        self._next_time = perf_counter() + self.get_interval()
        self._last_time = 0

    cpdef attempt(self):
        cdef bool result = False
        cdef double now = perf_counter()

        if now >= self._next_time:
            self._next_time = now + self.get_interval()
            result = True

        self._last_time = now
        return result

    cpdef double get_interval(self):
        return max(gcv(self._interval), 0)

    @property
    def interval(self) -> double:
        return self.get_interval()

    @property
    def last_time(self) -> double:
        return self._last_time

    cpdef double get_progress(self):
        return max(0, min(1, (perf_counter() - self.last_time) / self.get_interval()))

    @property
    def progress(self) -> double:
        return self.get_progress()


cdef class FixedTimer:
    cdef object __weakref__
    cdef float _interval, _start_time
    cdef int _max_lag, _count

    def __init__(
        self,
        interval: float,
        max_lag: int = 10,
    ):
        if interval <= 0:
            raise ValueError("Interval must be positive")

        self._interval = interval
        self._max_lag = max_lag
        self._count = 0
        self._start_time = perf_counter()

    cpdef attempt(self):
        cdef int ideal_ticks_int

        if self.ideal_ticks > self._count:
            if (
                ideal_ticks_int := math.floor(self.ideal_ticks)
            ) - self._count > self._max_lag:
                self._count = ideal_ticks_int - self._max_lag
            self._count += 1
            return True

        return False

    @property
    def interval(self):
        return self._interval

    @property
    def tick(self) -> int:
        return self._count

    cpdef float get_ideal_ticks(self):
        return (perf_counter() - self._start_time) / self._interval

    @property
    def ideal_ticks(self) -> float:
        return self.get_ideal_ticks()

    cpdef float get_progress_by_tick(self, tick: t.Optional[int]):
        return 1 if tick is None else (1 - max(0, min(1, tick - self.ideal_ticks)))

    @property
    def progress(self) -> float:
        return self.get_progress_by_tick(self.tick)
