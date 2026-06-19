import asyncio
import typing as t

import pytest

from FloriaKit.utils import (
    coalapse,
    coalapse_lazy,
    invoke,
    partition,
    ensure_iterable,
    yield_every,
    try_import,
)


# ---------------------------------------------------------------------------
# coalapse
# ---------------------------------------------------------------------------
class TestCoalapse:
    def test_returns_first_not_none(self) -> None:
        result = coalapse(None, None, 42, None)
        assert result == 42

    def test_raises_default_exception_when_all_none_and_no_default(self) -> None:
        with pytest.raises(ValueError):
            coalapse(None, None)

    def test_returns_default_when_all_none(self) -> None:
        result = coalapse(None, None, default=100)
        assert result == 100

    def test_raises_custom_exception_instance(self) -> None:
        class CustomError(Exception):
            pass

        exc = CustomError("custom message")
        with pytest.raises(CustomError, match="custom message"):
            coalapse(None, None, exception=exc)

    def test_raises_custom_exception_string(self) -> None:
        with pytest.raises(Exception, match="SomeError"):
            coalapse(None, None, exception="SomeError")


# ---------------------------------------------------------------------------
# coalapse_lazy
# ---------------------------------------------------------------------------
class TestCoalapseLazy:
    def test_returns_first_not_none_value(self) -> None:
        result = coalapse_lazy(None, None, 5, None)
        assert result == 5

    def test_returns_default_when_all_none(self) -> None:
        result = coalapse_lazy(None, None, default=7)
        assert result == 7

    def test_raises_value_error_when_all_none_no_default(self) -> None:
        with pytest.raises(ValueError):
            coalapse_lazy(None, None)

    def test_respects_calculated_value(self) -> None:
        def lazy_10() -> int:
            return 10

        def lazy_none() -> None:
            return None

        result = coalapse_lazy(lazy_none, lazy_10, None)
        assert result == 10
        assert result == 10

    def test_calculated_value_is_called_only_if_needed(self) -> None:
        side_effects: t.List[str] = []

        def lazy_fail() -> None:
            side_effects.append("fail")
            return None

        def lazy_ok() -> int:
            side_effects.append("ok")
            return 42

        result = coalapse_lazy(lazy_fail, lazy_ok)
        assert result == 42
        assert side_effects == ["fail", "ok"]

        side_effects.clear()
        result = coalapse_lazy(1, lazy_fail, lazy_ok)
        assert result == 1
        assert side_effects == []  # ни один ленивый не был вызван

    def test_raises_custom_exception_instance(self) -> None:
        exc = RuntimeError("runtime error")
        with pytest.raises(RuntimeError, match="runtime error"):
            coalapse_lazy(None, None, exception=exc)

    def test_raises_custom_exception_string(self) -> None:
        with pytest.raises(Exception, match="CustomError"):
            coalapse_lazy(None, None, exception="CustomError")


# ---------------------------------------------------------------------------
# invoke
# ---------------------------------------------------------------------------
class TestInvoke:
    @pytest.mark.asyncio
    async def test_invoke_sync_function(self) -> None:
        def sync_add(a: int, b: int) -> int:
            return a + b

        result = await invoke(sync_add, 2, 3)
        assert result == 5

    @pytest.mark.asyncio
    async def test_invoke_coroutine_function(self) -> None:
        async def async_mul(a: int, b: int) -> int:
            await asyncio.sleep(0)
            return a * b

        result = await invoke(async_mul, 3, 4)
        assert result == 12

    @pytest.mark.asyncio
    async def test_invoke_passes_arguments_correctly(self) -> None:
        def concat(a: str, b: str, *, sep: str = "-") -> str:
            return f"{a}{sep}{b}"

        result = await invoke(concat, "hello", "world", sep=" ")
        assert result == "hello world"


# ---------------------------------------------------------------------------
# partition
# ---------------------------------------------------------------------------
class TestPartition:
    def test_partition_with_predicate(self) -> None:
        pred: t.Callable[[int], bool] = lambda x: x > 5
        trues, falses = partition(pred, [1, 8, 3, 10])
        assert trues == [8, 10]
        assert falses == [1, 3]

    def test_partition_with_none_predicate_removes_none(self) -> None:
        trues, falses = partition(None, [1, None, 2, None, 3])
        assert trues == [1, 2, 3]
        assert falses == [None, None]

    def test_partition_all_true(self) -> None:
        trues, falses = partition(lambda x: True, [1, 2])
        assert trues == [1, 2]
        assert falses == []

    def test_partition_empty_iterable(self) -> None:
        trues, falses = partition(bool, [])
        assert trues == []
        assert falses == []


# ---------------------------------------------------------------------------
# ensure_iterable
# ---------------------------------------------------------------------------
class TestEnsureIterable:
    def test_string_becomes_list(self) -> None:
        result = ensure_iterable("hello")
        assert result == ["hello"]

    def test_bytes_becomes_list(self) -> None:
        result = ensure_iterable(b"abc")
        assert result == [b"abc"]

    def test_non_string_iterable_remains_unchanged(self) -> None:
        lst = [1, 2, 3]
        result = ensure_iterable(lst)
        assert result is lst

    def test_set_remains_unchanged(self) -> None:
        s = {1, 2}
        result = ensure_iterable(s)
        assert result is s

    def test_non_iterable_becomes_list(self) -> None:
        result = ensure_iterable(42)
        assert result == [42]


# ---------------------------------------------------------------------------
# yield_every
# ---------------------------------------------------------------------------
class TestYieldEvery:
    @pytest.mark.asyncio
    async def test_yields_all_items(self) -> None:
        items = list(range(5))
        collected: t.List[int] = []
        async for item in yield_every(items, step=2, pause=0):
            collected.append(item)
        assert collected == items

    @pytest.mark.asyncio
    async def test_step_pause_effect(self) -> None:
        """Проверяем, что asyncio.sleep вызывается нужное количество раз."""
        items = list(range(10))
        sleep_call_count = 0
        original_sleep = asyncio.sleep

        async def counting_sleep(delay: float) -> None:
            nonlocal sleep_call_count
            sleep_call_count += 1
            await original_sleep(0)

        asyncio.sleep = counting_sleep
        try:
            async for _ in yield_every(items, step=3, pause=0.1):
                pass
            assert sleep_call_count == 4
        finally:
            asyncio.sleep = original_sleep

    @pytest.mark.asyncio
    async def test_progress_callback_is_called(self) -> None:
        items = ["a", "b", "c"]
        callback_calls: t.List[t.Tuple[int, str]] = []

        async def progress_callback(index: int, item: str) -> None:
            callback_calls.append((index, item))

        async for _ in yield_every(
            items, step=1, pause=0, progress_callback=progress_callback
        ):
            pass
        assert callback_calls == [(0, "a"), (1, "b"), (2, "c")]

    @pytest.mark.asyncio
    async def test_invalid_step_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Step must be non-negative"):
            async for _ in yield_every([1], step=0):
                pass


# ---------------------------------------------------------------------------
# try_import
# ---------------------------------------------------------------------------
class TestTryImport:
    def test_successful_import_does_nothing(self) -> None:
        with try_import():
            import sys
        assert True

    def test_import_error_without_exception_reraises(self) -> None:
        with pytest.raises(ImportError):
            with try_import():
                import nonexistent_module  # pyright: ignore[reportMissingImports]

    def test_import_error_with_string_exception(self) -> None:
        with pytest.raises(Exception, match="SomeError"):
            with try_import(exception="SomeError"):
                import nonexistent_module  # pyright: ignore[reportMissingImports]

    def test_import_error_with_instance_exception(self) -> None:
        exc = ValueError("instance error")
        with pytest.raises(ValueError, match="instance error"):
            with try_import(exception=exc):
                import nonexistent_module  # pyright: ignore[reportMissingImports]

    def test_other_exceptions_not_caught(self) -> None:
        with pytest.raises(ZeroDivisionError):
            with try_import():
                _ = 1 / 0
