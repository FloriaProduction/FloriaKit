import typing as t
import weakref
import asyncio
import inspect

from . import function


P = t.ParamSpec('P', default=[])
R = t.TypeVar('R', default=t.Any)


cdef class EventHandlerInfo:
    cdef object weak_func # weakref.ReferenceType | callable
    cdef bint once

    def __init__(
        self, 
        object handler, 
        bint once = False, 
        bint weak = True
    ) -> None:
        self.weak_func = weakref.WeakMethod(handler) if hasattr(handler, '__self__') and weak else handler
        self.once = once

    cdef get_func(self):
        return func() if isinstance(func := self.weak_func, weakref.ReferenceType) else func


cdef class EventAsyncHandlerInfo(EventHandlerInfo):
    cdef bint wait

    def __init__(
        self, 
        object handler, 
        bint once = False, 
        bint wait = True, 
        bint weak = True
    ) -> None:
        super().__init__(handler=handler, once=once, weak=weak)

        self.wait = wait


cdef class _BaseEvent:
    cdef object __weakref__
    cdef dict[str, EventHandlerInfo] _handlers
    cdef bint _is_invoked

    def __init__(self):
        self._handlers = {}
        self._is_invoked = False

    def register(self, handler=None, *, once: bool = False, wait: bool = True, weak: bool = True, override: bool = False):
        def decorator(func):
            if override or (key := function.get_key(func)) not in self._handlers:
                if self.is_invoking:
                    raise RuntimeError("Cannot register handler while event is being invoked")
                self._handlers[key] = EventHandlerInfo(
                    handler=func,
                    once=once,
                    wait=wait,
                    weak=weak,
                )
            return func

        if handler is None:
            return decorator
        return decorator(handler)

    def unregister(self, handler=None):
        if handler is not None:
            key = function.get_key(handler)
            if key in self._handlers:
                if self.is_invoking:
                    raise RuntimeError("Cannot unregister handler while event is being invoked")
                self._handlers.pop(key)
        return handler

    def __call__(self, func):
        return self.register(func)

    cpdef bool has_key(self, key: str | None):
        return key is not None and key in self._handlers

    cpdef bool has(self, object func):
        return False if func is None else self.has_key(function.get_key(func))

    def __len__(self):
        return len(self._handlers)

    def clear(self):
        self._handlers.clear()

    @property
    def is_invoking(self):
        return self._is_invoked

cdef class _Event(_BaseEvent):
    cdef dict[str, EventHandlerInfo] _handlers

    def __init__(self):
        super().__init__()
        self._handlers = {}

    def register(self, handler=None, *, once: bool = False, weak: bool = True, override: bool = False):
        def decorator(func):
            key = function.get_key(func)
            if override or key not in self._handlers:
                if self.is_invoking:
                    raise RuntimeError("Cannot register handler while event is being invoked")
                self._handlers[key] = EventHandlerInfo(
                    handler=func,
                    once=once,
                    weak=weak,
                )
            return func

        if handler is None:
            return decorator
        return decorator(handler)

    def unregister(self, handler=None):
        if handler is not None:
            key = function.get_key(handler)
            if key in self._handlers:
                if self.is_invoking:
                    raise RuntimeError("Cannot unregister handler while event is being invoked")
                self._handlers.pop(key)
        return handler

    def __call__(self, func):
        return self.register(func)

    cpdef bool has_key(self, key: str | None):
        return key is not None and key in self._handlers

    cpdef bool has(self, object func):
        return False if func is None else self.has_key(function.get_key(func))

    def __len__(self):
        return len(self._handlers)

    def clear(self):
        self._handlers.clear()

    cpdef _invoke(self, tuple args, dict kw):
        cdef str key
        cdef EventHandlerInfo info
        cdef object handler, result, task

        cdef set[str] to_remove = set()

        self._is_invoked = True

        for key, info in self._handlers.items():
            if (handler := info.get_func()) is None:
                continue
            
            if info.once or handler is None:
                to_remove.add(key)

            handler(*args, **kw)

        if to_remove:
            for key in to_remove:
                self._handlers.pop(key, None)

        self._is_invoked = False

class Event(_Event, t.Generic[P, R]):
    def invoke(self, *args, **kwargs):
        self._invoke(args, kwargs)
        return self

cdef class _EventAsync(_BaseEvent):
    cdef dict[str, EventAsyncHandlerInfo] _handlers

    def __init__(self):
        super().__init__()
        self._handlers = {}

    def register(self, handler=None, *, once: bool = False, wait: bool = True, weak: bool = True, override: bool = False):
        def decorator(func):
            key = function.get_key(func)
            if override or key not in self._handlers:
                if self.is_invoking:
                    raise RuntimeError("Cannot register handler while event is being invoked")
                self._handlers[key] = EventAsyncHandlerInfo(
                    handler=func,
                    once=once,
                    wait=wait,
                    weak=weak,
                )
            return func

        if handler is None:
            return decorator
        return decorator(handler)

    def unregister(self, handler=None):
        if handler is not None:
            key = function.get_key(handler)
            if key in self._handlers:
                if self.is_invoking:
                    raise RuntimeError("Cannot unregister handler while event is being invoked")
                self._handlers.pop(key)
        return handler

    def __call__(self, func):
        return self.register(func)

    cpdef bool has_key(self, key: str | None):
        return key is not None and key in self._handlers

    cpdef bool has(self, object func):
        return False if func is None else self.has_key(function.get_key(func))

    def __len__(self):
        return len(self._handlers)

    def clear(self):
        self._handlers.clear()

    cpdef list _invoke(self, tuple args, dict kw):
        cdef str key
        cdef EventAsyncHandlerInfo info
        cdef object handler, cor

        cdef set[str] to_remove = set()
        cdef list[t.Coroutine[t.Any, t.Any, t.Any]] cors = list()

        self._is_invoked = True

        for key, info in self._handlers.items():
            if (handler := info.get_func()) is None:
                to_remove.add(key)
                continue
            
            if info.once:
                to_remove.add(key)


            if not inspect.iscoroutinefunction(handler):
                raise TypeError(f"Handler {handler.__qualname__} did not return a coroutine")

            cor = handler(*args, **kw)

            if info.wait:
                cors.append(cor)
            else:
                asyncio.create_task(cor).add_done_callback(self._task_done_callback)

        if to_remove:
            for key in to_remove:
                self._handlers.pop(key, None)

        self._is_invoked = False

        return cors

    @staticmethod
    def _task_done_callback(task: asyncio.Task[t.Any]):
        try:
            task.result()
        except asyncio.CancelledError:
            pass

class EventAsync(_EventAsync, t.Generic[P, R]):
    async def invoke(self, *args, **kwargs):
        if (cors := self._invoke(args, kwargs)):
            await asyncio.gather(*cors, return_exceptions=True)
        return self


# class EventAny(BaseEvent, t.Generic[P, R]):
#     def __init__(self):
#         super().__init__(True)

#     async def invoke_async(self, *args, **kwargs):
#         if (tasks := self._invoke(args, kwargs)):
#             await asyncio.gather(*tasks)

#     def invoke_sync(self, *args, **kwargs):
#         self._invoke(args, kwargs)
