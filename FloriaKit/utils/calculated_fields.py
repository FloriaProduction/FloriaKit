import typing as t

from .interpolation_field import InterpolationField
from .calculated_value import CalculatedValue, gcv


class CalculatedFields[TK: str = str, **P = []]:
    __slots__ = (
        '_map',
        '_process_func',
        '__weakref__',
    )

    @staticmethod
    def default_process(value: t.Any) -> t.Any:
        if isinstance(value, InterpolationField):
            return t.cast(InterpolationField[t.Any], value).get_value()

        elif isinstance(value, CalculatedValue):
            return gcv(t.cast(CalculatedValue[t.Any], value))

        return value

    def __init__(
        self,
        map: t.Mapping[TK | str, CalculatedValue[t.Any, P] | t.Any] | None = None,
        process_func: t.Callable[[t.Any], t.Any] | None = None,
    ):
        self._map: dict[TK | str, CalculatedValue[t.Any, P] | t.Any] = (
            {}
            if map is None
            else t.cast(dict[TK | str, CalculatedValue[t.Any, P] | t.Any], map)
        )
        self._process_func: t.Callable[[t.Any], t.Any] | None = process_func

    def update(
        self,
        map: t.Mapping[TK | str, CalculatedValue[t.Any, P] | t.Any],
    ) -> t.Self:
        self._map.update(map)
        return self

    def get[TD: t.Any | None = None](
        self,
        name: TK | str,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> t.Any | TD:
        if (func := self._map.get(name)) is None:
            return None

        value = gcv(func, *args, **kwargs)

        return (
            value
            if (process_func := self._process_func) is None
            else process_func(value)
        )

    @property
    def names(self) -> list[TK | str]:
        return list(self._map.keys())


__all__ = ['CalculatedFields']
