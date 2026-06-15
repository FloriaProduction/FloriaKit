import typing as t
from abc import ABC


class ReprMixin(ABC):
    __slots__ = ()

    def _get_repr_kw(self) -> t.Mapping[str, t.Any]:
        return {}

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({'; '.join(f'{key}: {value}' for key, value in self._get_repr_kw().items())})'


__all__ = ['ReprMixin']
