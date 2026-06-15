import typing as t


cdef class Avg:
    cdef float _sum
    cdef int _count

    def __init__(self) -> None:
        self._sum = 0
        self._count = 0

    cpdef add(self, float value):
        self._sum += value
        self._count += 1

        return self

    cpdef extend(self, values: t.Iterable[float]):
        for value in values:
            self.add(value)

        return self

    cpdef clear(self):
        self._sum = 0
        self._count = 0

        return self

    @property
    def count(self) -> int:
        return self._count

    @property
    def total(self) -> float:
        return self._sum

    cpdef get_value(self):
        return self._sum / self._count if self._count > 0 else 0

    @property
    def value(self) -> float:
        return self.get_value()

    def __len__(self) -> int:
        return self._count

    def __iadd__(self, value: float) -> 'Avg':
        self.add(value)
        return self

