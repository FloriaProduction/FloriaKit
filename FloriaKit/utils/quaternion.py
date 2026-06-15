import typing as t

from .common import try_import

if t.TYPE_CHECKING:
    from .. import hints

with try_import(ModuleNotFoundError("Install the PyGLM package: pip install pyglm")):
    from pyglm import glm


def look_at(
    eye: 'hints.pos3',
    target: 'hints.pos3',
    up: 'hints.pos3' = (0, 1, 0),
) -> 'hints.quat':
    return tuple(
        glm.inverse(
            glm.quat(glm.lookAt(eye, target, up)),
        )
    )  # pyright: ignore[reportReturnType]


def slerp(
    start: 'hints.quat',
    end: 'hints.quat',
    progress: float,
) -> 'hints.quat':
    return tuple(
        glm.slerp(
            start,
            end,
            progress,
        )
    )  # pyright: ignore[reportReturnType]


def lerp(
    start: 'hints.quat',
    end: 'hints.quat',
    progress: float,
) -> 'hints.quat':
    return tuple(
        glm.lerp(
            start,
            end,
            progress,
        )
    )  # pyright: ignore[reportReturnType]


def from_euler(
    angle: 'hints.vec3',
) -> 'hints.quat':
    return tuple(glm.quat(angle))  # pyright: ignore[reportReturnType]


def from_axis_angle(
    axis: 'hints.vec3',
    angle: float,
) -> 'hints.quat':
    return tuple(
        glm.angleAxis(
            angle,
            axis,
        )
    )  # pyright: ignore[reportReturnType]


__all__ = [
    'look_at',
    'slerp',
    'lerp',
    'from_euler',
    'from_axis_angle',
]
