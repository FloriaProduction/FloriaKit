import typing as t
from uuid import UUID, uuid4

from .dispose import DisposeMixin
from .id import IDMixin


class DisposeIDMixin[TID](DisposeMixin, IDMixin[TID]):
    __slots__ = ()

    def dispose(self) -> bool:
        if self.is_disposed:
            return False

        self._id = None

        return True

    @property
    def is_disposed(self) -> bool:
        return self._id is None


class DisposeUUIDIDMixin(DisposeIDMixin[UUID]):
    __slots__ = ()

    def _generate_id(self):
        return uuid4()


class DisposeIntIDMixin(DisposeIDMixin[int]):
    __slots__ = ()
    __next_id: int = 0

    def _generate_id(self):
        id = DisposeIntIDMixin.__next_id
        DisposeIntIDMixin.__next_id += 1
        return id


__all__ = [
    'DisposeIDMixin',
    'DisposeUUIDIDMixin',
    'DisposeIntIDMixin',
]
