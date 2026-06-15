import typing as t

from .calculated_value import CalculatedValue, gcv


class CalculatedField[T = t.Any]:
    __slots__ = (
        '_value',
        '_value_cache',
        '__weakref__',
    )

    def __init__(self, value: T | CalculatedValue[T]):
        self._value = value
        self._value_cache: T = gcv(self._value)

    def get_value(self) -> T:
        return self._value_cache

    def set_value(self, value: T | CalculatedValue[T]) -> t.Self:
        self._value = value
        return self

    def update(self):
        self._value_cache = gcv(self._value)

    @property
    def is_interpolated(self):
        if not isinstance(self._value, CalculatedValue):
            return False

        if (value := gcv(self._value)) != self._value_cache:  # type: ignore
            self._value_cache = value
            return True
        return False


__all__ = ['CalculatedField']
