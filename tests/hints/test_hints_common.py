import typing as t
import gc
import pathlib

from FloriaKit.hints.common import (
    PathOrStr,
    get_path,
    #
    Ref,
    to_ref,
    from_ref,
)


class TestPath:
    def test_str_converts_to_path(self):
        result = get_path("foo/bar/baz.txt")
        assert isinstance(result, pathlib.Path)
        assert result == pathlib.Path("foo/bar/baz.txt")

    def test_path_is_returned_as_is(self):
        p = pathlib.Path("another/file.txt")
        result = get_path(p)
        assert result is p

    def test_empty_string(self):
        result = get_path("")
        assert isinstance(result, pathlib.Path)
        assert result == pathlib.Path("")

    def test_path_with_special_characters(self):
        result = get_path("dir with spaces/and/中文")
        assert result == pathlib.Path("dir with spaces/and/中文")


class TestRef:
    class AliveObject:
        pass

    def test_to_ref_returns_weakref_for_live_object(self):
        obj = self.AliveObject()
        ref = to_ref(obj)

        assert isinstance(ref, Ref)
        assert ref() is obj

    def test_to_ref_returns_none_for_none(self):
        assert to_ref(None) is None

    def test_to_ref_callback_is_called_when_object_dies(self):
        called: list[t.Any] = []

        def callback(ref: Ref[t.Any]):
            called.append(True)

        obj = self.AliveObject()
        ref = to_ref(obj, callback=callback)  # pyright: ignore[reportUnusedVariable]

        del obj
        gc.collect()

        assert len(called) == 1

    def test_from_ref_returns_object_for_live_ref(self):
        obj = self.AliveObject()
        ref = to_ref(obj)

        assert from_ref(ref) is obj

    def test_from_ref_returns_none_when_ref_is_none(self):
        assert from_ref(None) is None

    def test_from_ref_returns_none_when_referent_is_dead(self):
        obj = self.AliveObject()
        ref = to_ref(obj)

        del obj
        gc.collect()

        assert from_ref(ref) is None

    def test_to_ref_then_from_ref_roundtrip(self):
        original = self.AliveObject()
        assert from_ref(to_ref(original)) is original

    def test_from_ref_on_already_dead_ref(self):
        obj = self.AliveObject()
        ref = Ref(obj)
        del obj
        gc.collect()

        assert from_ref(ref) is None
