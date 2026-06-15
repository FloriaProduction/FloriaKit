import typing as t

from .dispose import HasDispose
from .id import HasID


class HasDisposeID[TID = t.Any](HasDispose, HasID[TID], t.Protocol): ...


__all__ = ['HasDisposeID']
