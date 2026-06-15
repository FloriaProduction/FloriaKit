import typing as t


cdef class Flag:
    cdef int _depth

    def __init__(self):
        self._depth = 0

    def __enter__(self, *args: t.Any, **kwargs: t.Any):
        self._depth += 1

    def __exit__(self, *args: t.Any, **kwargs: t.Any):
        self._depth -= 1

    @property
    def value(self) -> bool:
        return self._depth > 0

    def __bool__(self) -> bool:
        return self.value

