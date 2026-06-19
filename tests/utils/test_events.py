import asyncio
import gc
import weakref
import typing as t
import pytest

from FloriaKit.utils.events import Event, EventAsync


def sync_collector(calls: list[t.Any]):
    def handler(*args: t.Any, **kwargs: t.Any):
        calls.append((args, kwargs))

    return handler


async def async_collector(calls: list[t.Any]):
    async def handler(*args: t.Any, **kwargs: t.Any):
        calls.append((args, kwargs))

    return handler


@pytest.fixture
def event() -> Event:
    return Event()


@pytest.fixture
def async_event() -> EventAsync:
    return EventAsync()


class TestEventBasic:
    def test_initial_empty(self, event: Event):
        assert len(event) == 0

    def test_register_direct(self, event: Event):
        calls: list[t.Any] = []
        h = sync_collector(calls)
        returned = event.register(h)
        assert returned is h
        assert len(event) == 1
        assert event.has(h)

    def test_register_as_decorator(self, event: Event):
        calls: list[t.Any] = []

        @event
        def handler(*args: t.Any, **kwargs: t.Any):
            calls.append((args, kwargs))

        assert len(event) == 1
        assert event.has(handler)

    def test_unregister_existing(self, event: Event):
        calls: list[t.Any] = []
        h = sync_collector(calls)
        event.register(h)
        returned = event.unregister(h)
        assert returned is h
        assert len(event) == 0
        assert not event.has(h)

    def test_unregister_none_does_nothing(self, event: Event):
        calls: list[t.Any] = []
        h = sync_collector(calls)
        event.register(h)
        returned = event.unregister(None)
        assert returned is None
        assert len(event) == 1
        assert event.has(h)

    def test_clear(self, event: Event):
        h1 = sync_collector([])
        h2 = sync_collector([])
        event.register(h1)
        event.register(h2)
        event.clear()
        assert len(event) == 0
        assert not event.has(h1)
        assert not event.has(h2)

    def test_len_reflects_handlers(self, event: Event):
        h = sync_collector([])
        event.register(h)
        assert len(event) == 1
        event.unregister(h)
        assert len(event) == 0


class TestEventInvoke:
    def test_invoke_calls_all_handlers(self, event: Event[...]):
        calls: list[t.Any] = []
        h1 = sync_collector(calls)
        h2 = sync_collector(calls)
        event.register(h1)
        event.register(h2)
        result = event.invoke(1, a=2)
        assert result is event
        assert len(calls) == 2
        assert calls[0] == ((1,), {"a": 2})
        assert calls[1] == ((1,), {"a": 2})

    def test_invoke_once_handler_removed_after_call(self, event: Event[...]):
        calls: list[t.Any] = []
        h = sync_collector(calls)
        event.register(once=True)(h)
        event.invoke(42)
        assert len(calls) == 1
        assert len(event) == 0
        assert not event.has(h)

    def test_invoke_once_multiple_calls(self, event: Event[...]):
        calls: list[t.Any] = []
        h = sync_collector(calls)
        event.register(once=True)(h)
        event.invoke(1)
        event.invoke(2)
        assert len(calls) == 1  # второй вызов не должен случиться

    def test_is_invoking_flag(self, event: Event):
        states: list[t.Any] = []

        def check_flag(*args: t.Any):
            states.append(event.is_invoking)

        event.register(check_flag)
        assert not event.is_invoking
        event.invoke()
        assert states == [True]
        assert not event.is_invoking


class TestEventOverride:
    def test_override_replaces_options(self, event: Event[...]):
        calls: list[t.Any] = []
        h = sync_collector(calls)
        event.register(once=False)(h)
        # Переопределяем с once=True
        event.register(override=True, once=True)(h)
        # Должен остаться один обработчик
        assert len(event) == 1

        event.invoke()
        # После одного вызова обработчик удалён
        assert len(event) == 0
        assert not event.has(h)


class TestEventAsyncBasic:
    @pytest.mark.asyncio
    async def test_initial_empty(self, async_event: EventAsync):
        assert len(async_event) == 0

    @pytest.mark.asyncio
    async def test_register_direct(self, async_event: EventAsync):
        calls: list[t.Any] = []
        h = await async_collector(calls)
        returned = async_event.register(h)
        assert returned is h
        assert len(async_event) == 1
        assert async_event.has(h)

    @pytest.mark.asyncio
    async def test_register_as_decorator(self, async_event: EventAsync[...]):
        calls: list[t.Any] = []

        @async_event
        async def handler(*args: t.Any, **kwargs: t.Any):
            calls.append((args, kwargs))

        assert len(async_event) == 1
        assert async_event.has(handler)

    @pytest.mark.asyncio
    async def test_unregister_existing(self, async_event: EventAsync):
        calls: list[t.Any] = []
        h = await async_collector(calls)
        async_event.register(h)
        returned = async_event.unregister(h)
        assert returned is h
        assert len(async_event) == 0
        assert not async_event.has(h)

    @pytest.mark.asyncio
    async def test_clear(self, async_event: EventAsync):
        h1 = await async_collector([])
        h2 = await async_collector([])
        async_event.register(h1)
        async_event.register(h2)
        async_event.clear()
        assert len(async_event) == 0


class TestEventAsyncInvoke:
    @pytest.mark.asyncio
    async def test_invoke_calls_all_handlers(self, async_event: EventAsync[...]):
        calls: list[t.Any] = []
        h1 = await async_collector(calls)
        h2 = await async_collector(calls)
        async_event.register(h1)
        async_event.register(h2)
        result = await async_event.invoke(1, a=2)
        assert result is async_event
        assert len(calls) == 2

    @pytest.mark.asyncio
    async def test_invoke_once_removes_handler(self, async_event: EventAsync[...]):
        calls: list[t.Any] = []
        h = await async_collector(calls)
        async_event.register(once=True)(h)
        await async_event.invoke(42)
        assert len(calls) == 1
        assert len(async_event) == 0

    @pytest.mark.asyncio
    async def test_wait_true_sequential_execution(self, async_event: EventAsync[...]):
        """
        Если wait=True (по умолчанию), вызовы должны идти последовательно,
        и invoke возвращает управление только после завершения всех обработчиков.
        """
        order: list[t.Any] = []

        async def first():
            order.append(1)
            await asyncio.sleep(0.01)

        async def second():
            order.append(2)

        async_event.register(wait=True)(first)
        async_event.register(wait=True)(second)
        await async_event.invoke()
        assert order == [1, 2]

    @pytest.mark.asyncio
    async def test_wait_false_returns_immediately(self, async_event: EventAsync[...]):
        """
        При wait=False invoke не ждёт завершения корутины.
        Проверяем, что обработчик ещё не отработал на момент возврата.
        """
        done: list[t.Any] = []

        async def slow():
            await asyncio.sleep(0.05)
            done.append(True)

        async_event.register(wait=False)(slow)
        await async_event.invoke()
        # Сразу после invoke обработчик ещё не завершён
        assert done == []


class TestEventAsyncAdvanced:
    @pytest.mark.asyncio
    async def test_override_replaces_options(self, async_event: EventAsync[...]):
        calls: list[t.Any] = []
        h = await async_collector(calls)
        async_event.register(once=False)(h)
        async_event.register(override=True, once=True)(h)
        assert len(async_event) == 1
        await async_event.invoke()
        assert len(async_event) == 0
