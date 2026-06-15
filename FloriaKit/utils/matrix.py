import typing as t

from .common import try_import

if t.TYPE_CHECKING:
    from .. import hints

with try_import(ModuleNotFoundError("Install the PyGLM package: pip install pyglm")):
    from pyglm import glm


def model_matrix(
    position: 'hints.pos3',
    angle: 'hints.quat',
    scale: 'hints.scale3',
    origin: 'hints.pos3' = (0, 0, 0),
) -> 'hints.mat4x4':
    return tuple(
        glm.translate(glm.mat4(1), position)
        * glm.mat4_cast(angle)
        * glm.scale(glm.mat4(1.0), scale)
        * glm.translate(tuple(o / s if s != 0 else 0 for o, s in zip(origin, scale)))
    )  # pyright: ignore[reportReturnType]


def view_matrix(
    position: 'hints.pos3',
    angle: 'hints.quat',
) -> 'hints.mat4x4':
    return tuple(
        glm.lookAt(
            position,
            glm.vec3(*position) + (rotation_glm := glm.quat(*angle)) * (0.0, 0.0, -1.0),
            rotation_glm * (0.0, 1.0, 0.0),
        )
    )  # pyright: ignore[reportReturnType]


def ortho_projection_matrix(
    size: 'hints.size2',
    near_far: tuple[float, float],
    zoom: float = 1,
) -> 'hints.mat4x4':
    width, height = size
    return tuple(
        glm.ortho(
            -width / 2 / zoom,
            width / 2 / zoom,
            -height / 2 / zoom,
            height / 2 / zoom,
            *near_far,
        )
    )  # pyright: ignore[reportReturnType]


def perspective_projection_matrix(
    fov: float,
    aspect: float,
    near_far: tuple[float, float],
    zoom: float = 1,
) -> 'hints.mat4x4':
    return tuple(
        glm.perspective(
            glm.radians(fov / zoom),
            aspect,
            *near_far,
        )
    )  # pyright: ignore[reportReturnType]


__all__ = [
    'model_matrix',
    'view_matrix',
    'ortho_projection_matrix',
    'perspective_projection_matrix',
]
