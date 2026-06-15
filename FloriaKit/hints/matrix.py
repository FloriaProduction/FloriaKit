import typing as t

from .common import vec2, vec3, vec4

type mat2x2 = tuple[vec2, vec2]
type mat3x3 = tuple[vec3, vec3, vec3]
type mat4x4 = tuple[vec4, vec4, vec4, vec4]


__all__ = [
    'mat2x2',
    'mat3x3',
    'mat4x4',
]
