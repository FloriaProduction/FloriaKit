import typing as t
from abc import ABC, abstractmethod
from uuid import UUID, uuid4


class HasID[T: t.Any](t.Protocol):
    @property
    def id(self) -> T: ...


__all__ = [
    'HasID',
]
