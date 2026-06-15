import math
import typing as t

import pytest

from FloriaKit.utils.quaternion import (
    look_at,
    slerp,
    lerp,
    from_euler,
    from_axis_angle,
)


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------
def quat_length(q: t.Tuple[float, float, float, float]) -> float:
    return math.sqrt(sum(c * c for c in q))


def quat_is_normalized(
    q: t.Tuple[float, float, float, float], tolerance: float = 1e-6
) -> bool:
    return abs(quat_length(q) - 1.0) < tolerance


def assert_quat_normalized(
    q: t.Tuple[float, float, float, float],
    abs_tol: float = 1e-6,
    rel_tol: float = 1e-6,
) -> None:
    length = quat_length(q)
    assert math.isclose(
        length, 1.0, rel_tol=rel_tol, abs_tol=abs_tol
    ), f"Quaternion length is {length}, expected ~1.0"


def assert_quat_close(
    q1: t.Tuple[float, float, float, float], q2: t.Tuple[float, float, float, float]
) -> None:
    close_same = all(
        math.isclose(a, b, rel_tol=1e-5, abs_tol=1e-5) for a, b in zip(q1, q2)
    )
    close_neg = all(
        math.isclose(a, -b, rel_tol=1e-5, abs_tol=1e-5) for a, b in zip(q1, q2)
    )
    assert close_same or close_neg, f"Quaternions differ: {q1} vs {q2}"


# ---------------------------------------------------------------------------
# Тесты look_at
# ---------------------------------------------------------------------------
class TestLookAt:
    def test_look_at_identity_no_rotation(self) -> None:
        q = look_at(
            eye=(0.0, 0.0, 0.0),
            target=(0.0, 0.0, -1.0),
            up=(0.0, 1.0, 0.0),
        )
        # Ожидаемый единичный кватернион (в glm порядок w,x,y,z)
        expected = (1.0, 0.0, 0.0, 0.0)
        assert isinstance(q, tuple)
        assert len(q) == 4
        assert all(isinstance(c, float) for c in q)
        assert_quat_normalized(q)
        assert_quat_close(q, expected)

    def test_look_at_returns_tuple_of_floats(self) -> None:
        q = look_at(
            eye=(1.0, 2.0, 3.0),
            target=(4.0, 5.0, 6.0),
            up=(0.0, 1.0, 0.0),
        )
        assert isinstance(q, tuple)
        assert len(q) == 4
        for c in q:
            assert isinstance(c, float)

    def test_look_at_normalized(self) -> None:
        q = look_at(eye=(10, 20, 30), target=(0, 0, 0), up=(1, 0, 0))
        assert_quat_normalized(q)

    def test_look_at_default_up(self) -> None:
        q1 = look_at(eye=(0, 0, 0), target=(0, 0, -1), up=(0, 1, 0))
        q2 = look_at(eye=(0, 0, 0), target=(0, 0, -1))  # up по умолчанию
        assert_quat_close(q1, q2)


# ---------------------------------------------------------------------------
# Тесты lerp
# ---------------------------------------------------------------------------
class TestLerp:
    def test_lerp_start_progress_zero(self) -> None:
        start = (1.0, 0.0, 0.0, 0.0)
        end = from_axis_angle((0.0, 1.0, 0.0), math.radians(45))
        result = lerp(start, end, 0.0)
        assert_quat_close(result, start)

    def test_lerp_end_progress_one(self) -> None:
        start = from_euler((0.0, 0.0, 0.0))
        end = from_axis_angle((0.0, 0.0, 1.0), math.radians(90))
        result = lerp(start, end, 1.0)
        assert_quat_close(result, end)

    def test_lerp_output_normalized(self) -> None:
        start = from_euler((0.1, 0.0, 0.0))
        end = from_euler((0.0, 0.2, 0.0))
        for t_val in (0.0, 0.5, 1.0):
            q = lerp(start, end, t_val)
            assert_quat_normalized(q, abs_tol=1e-2)

    def test_lerp_returns_tuple(self) -> None:
        start = (1.0, 0.0, 0.0, 0.0)
        end = (0.0, 0.0, 0.0, 1.0)
        r = lerp(start, end, 0.7)
        assert isinstance(r, tuple)
        assert len(r) == 4


# ---------------------------------------------------------------------------
# Тесты from_euler
# ---------------------------------------------------------------------------
class TestFromEuler:
    def test_zero_angles_gives_identity(self) -> None:
        q = from_euler((0.0, 0.0, 0.0))
        expected = (1.0, 0.0, 0.0, 0.0)
        assert_quat_close(q, expected)

    def test_returns_tuple_and_normalized(self) -> None:
        q = from_euler((math.radians(30), math.radians(45), math.radians(60)))
        assert isinstance(q, tuple)
        assert len(q) == 4
        assert_quat_normalized(q)


# ---------------------------------------------------------------------------
# Тесты from_axis_angle
# ---------------------------------------------------------------------------
class TestFromAxisAngle:
    def test_zero_angle_gives_identity(self) -> None:
        q = from_axis_angle((1.0, 0.0, 0.0), 0.0)
        expected = (1.0, 0.0, 0.0, 0.0)
        assert_quat_close(q, expected)

    def test_pi_rotation_around_x(self) -> None:
        q = from_axis_angle((1.0, 0.0, 0.0), math.pi)
        expected = (0.0, 1.0, 0.0, 0.0)
        assert_quat_close(q, expected)

    def test_returns_tuple_and_normalized_for_unit_axis(self) -> None:
        """Единичная ось даёт единичный кватернион."""
        q = from_axis_angle((0.0, 1.0, 0.0), math.radians(45))
        assert isinstance(q, tuple)
        assert len(q) == 4
        assert_quat_normalized(q)

    def test_non_unit_axis_produces_non_unit_quaternion(self) -> None:
        """PyGLM не нормализует ось автоматически – длина оси влияет на длину кватерниона."""
        q = from_axis_angle((3.0, 4.0, 0.0), math.radians(30))  # длина оси 5
        length = quat_length(q)
        # Длина не равна 1.0
        assert not math.isclose(
            length, 1.0, rel_tol=1e-3
        ), f"Expected non-unit quaternion for non-unit axis, got length {length}"

    def test_unit_axis_produces_unit_quaternion(self) -> None:
        """Нормализованная ось даёт единичный кватернион."""
        axis = (0.6, 0.8, 0.0)  # длина 1
        q = from_axis_angle(axis, math.radians(30))
        assert_quat_normalized(q)
