import typing as t

from .. import protocols as proto

class _BaseEvent:
    def __len__(self) -> int: ...
    def has_key(self, key: str | None) -> bool: ...
    def clear(self) -> None: ...
    @property
    def is_invoking(self) -> bool: ...

class Event[**P = [], R = t.Any](_BaseEvent):
    @t.overload
    def register(
        self,
        handler: proto.functions.SyncFunction[P, R],
        /,
    ) -> proto.functions.SyncFunction[P, R]: ...
    @t.overload
    def register(
        self,
        *,
        once: bool = False,
        weak: bool = True,
        override: bool = False,
    ) -> t.Callable[
        [proto.functions.SyncFunction[P, R]],
        proto.functions.SyncFunction[P, R],
    ]: ...
    def unregister[T: proto.functions.SyncFunction[..., t.Any]](
        self,
        handler: T | None = None,
    ) -> T | None: ...
    def __call__(
        self,
        func: proto.functions.SyncFunction[P, R],
    ) -> proto.functions.SyncFunction[P, R]: ...
    def has(
        self,
        func: proto.functions.SyncFunction[P, R] | None,
    ) -> bool: ...
    def invoke(self, *args: P.args, **kwargs: P.kwargs) -> t.Self: ...

class EventAsync[**P = [], R = t.Any](_BaseEvent):
    @t.overload
    def register(
        self,
        handler: proto.functions.AsyncFunction[P, R],
        /,
    ) -> proto.functions.AsyncFunction[P, R]: ...
    @t.overload
    def register(
        self,
        *,
        once: bool = False,
        wait: bool = True,
        weak: bool = True,
        override: bool = False,
    ) -> t.Callable[
        [proto.functions.AsyncFunction[P, R]],
        proto.functions.AsyncFunction[P, R],
    ]: ...
    def unregister[T: proto.functions.AsyncFunction[..., t.Any]](
        self,
        handler: T | None = None,
    ) -> T | None: ...
    def __call__(
        self,
        func: proto.functions.AsyncFunction[P, R],
    ) -> proto.functions.AsyncFunction[P, R]: ...
    def has(
        self,
        func: proto.functions.AsyncFunction[P, R] | None,
    ) -> bool: ...
    async def invoke(self, *args: P.args, **kwargs: P.kwargs) -> t.Self: ...

# class EventAny[**P = [], R = t.Any](BaseEvent[P, R]):
#     async def invoke_async(self, *args: P.args, **kwargs: P.kwargs) -> t.Self: ...
#     def invoke_sync(self, *args: P.args, **kwargs: P.kwargs) -> t.Self: ...

__all__ = [
    'Event',
    'EventAsync',
    # 'EventAny',
]
