import typing as t

from . import (
    color,
)

from .common import (
    number,
    #
    vec2,
    pos2,
    size2,
    scale2,
    vec2i,
    pos2i,
    size2i,
    scale2i,
    #
    vec3,
    pos3,
    size3,
    scale3,
    vec3i,
    pos3i,
    size3i,
    scale3i,
    #
    vec4,
    vec4i,
    #
    OneOrMany,
    #
    orientation,
    #
    PathOrStr,
    get_path,
    #
    Ref,
    to_ref,
    from_ref,
)
from .quaternion import quat
from .matrix import mat2x2, mat3x3, mat4x4
from .align import AlignSimple, AlignDetail, AlignAny, calculate_align
from .exception import ExceptionOrStr, get_exception
from .value_or_module import ValueOrModule, get_from_module

__all__ = [
    'color',
    #
    # common
    #
    'number',
    #
    'vec2',
    'pos2',
    'size2',
    'scale2',
    'vec2i',
    'pos2i',
    'size2i',
    'scale2i',
    #
    'vec3',
    'pos3',
    'size3',
    'scale3',
    'vec3i',
    'pos3i',
    'size3i',
    'scale3i',
    #
    'vec4',
    'vec4i',
    #
    'OneOrMany',
    #
    'orientation',
    #
    'PathOrStr',
    'get_path',
    #
    'Ref',
    'to_ref',
    'from_ref',
    #
    # quaternion
    #
    'quat',
    #
    # matrix
    #
    'mat2x2',
    'mat3x3',
    'mat4x4',
    #
    # align
    #
    'AlignSimple',
    'AlignDetail',
    'AlignAny',
    'calculate_align',
    #
    # exception
    #
    'ExceptionOrStr',
    'get_exception',
    #
    # value_or_module
    #
    'ValueOrModule',
    'get_from_module',
]
