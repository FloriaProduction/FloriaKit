import typing as t


class HasDispose(t.Protocol):
    def dispose(self) -> bool: ...

    @property
    def is_disposed(self) -> bool: ...


__all__ = ['HasDispose']
