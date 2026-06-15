import typing as t
import pytest

from FloriaKit.utils.events import Event


def make_sync_handler(base_value: int = 0):
    def handler(x: int = 0):
        return base_value + x

    return handler


@pytest.fixture
def event() -> Event:
    return Event()


def test_benchmark_event_invoke(event: Event[[int]], benchmark):
    event.register(make_sync_handler(10))

    benchmark(event.invoke, 42)


def test_benchmark_event_many_handlers(event: Event[[int]], benchmark):
    for i in range(100):
        event.register(make_sync_handler(1))

    benchmark(event.invoke, 1)
