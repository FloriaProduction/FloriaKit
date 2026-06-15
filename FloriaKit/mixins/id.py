import typing as t
from abc import ABC, abstractmethod
from uuid import UUID, uuid4


class IDMixin[T: t.Hashable](ABC):
    __slots__ = ('_id',)

    def __init__(self) -> None:
        super().__init__()

        self._id: T | None = self._generate_id()

    @abstractmethod
    def _generate_id(self) -> T: ...

    @property
    def id(self) -> T:
        if self._id is None:
            raise
        return self._id

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, IDMixin):
            return False
        return self.id == value.id  # type: ignore

    def __hash__(self) -> int:
        return hash(self.id)


class UUIDIDMixin(IDMixin[UUID]):
    __slots__ = ()

    def _generate_id(self):
        return uuid4()


__all__ = [
    'IDMixin',
    'UUIDIDMixin',
]
