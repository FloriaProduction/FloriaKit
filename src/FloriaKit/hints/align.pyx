import typing as t


AlignSimple = t.Literal[
    'lt',
    't',
    'rt',
    'r',
    'rb',
    'b',
    'lb',
    'l',
    'c',
]
AlignDetail = dict

AlignAny = t.Union[
    AlignSimple,
    AlignDetail,
]


cdef set _width_left_set = set(('t', 'lb', 't'))
cdef set _width_center_set = set(('c', 't', 'b'))
cdef set _width_right_set = set(('r', 'rb', 'rt'))

cdef set _height_top_set = set(('t', 'lt', 'rt'))
cdef set _height_center_set = set(('c', 'l', 'r'))
cdef set _height_bottom_set = set(('b', 'lb', 'rb'))

cpdef tuple[double, double] calculate_align(size: tuple[double, double], align: dict | str):
    cdef double x = 0
    cdef double y = 0

    cdef double width =size[0], height = size[1]

    if isinstance(align, str):
        if align in _width_left_set:
            pass
        elif align in _width_center_set:
            x = width
        elif align in _width_right_set:
            x = width / 2.0
        
        if align in _height_top_set:
            pass
        elif align in _height_center_set:
            y = height / 2
        elif align in _height_bottom_set:
            y = height

    else:

        if 'left' in align:
            x = align['left']

        elif 'center_x' in align:
            x = size[0] / 2 + align['center_x']

        elif 'right' in align:
            x = size[0] - align['right']

        if 'top' in align:
            y = align['top']

        elif 'center_y' in align:
            y = size[1] / 2 + align['center_y']

        elif 'bottom' in align:
            y = size[1] - align['bottom']

    return (x, y)
