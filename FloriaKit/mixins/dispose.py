import typing as t
from abc import ABC, abstractmethod
import contextlib


class DisposeMixin(ABC):
    __slots__ = ()

    @classmethod
    @contextlib.contextmanager
    def auto_dispose(cls, obj: t.Self, *args: t.Any, **kw: t.Any):
        try:
            yield obj

        finally:
            obj.dispose()

    def __del__(self):
        self.dispose()

    @abstractmethod
    def dispose(self) -> bool: ...

    @property
    @abstractmethod
    def is_disposed(self) -> bool: ...


__all__ = ['DisposeMixin']
