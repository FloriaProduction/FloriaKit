import typing as t

if t.TYPE_CHECKING:
    from .. import rgba

TRANSPARENT: 'rgba' = (0, 0, 0, 0)

RED: 'rgba' = (255, 0, 0, 255)
GREEN: 'rgba' = (0, 255, 0, 255)
BLUE: 'rgba' = (0, 0, 255, 255)

WHITE: 'rgba' = (255, 255, 255, 255)
BLACK: 'rgba' = (0, 0, 0, 255)


__all__ = [
    'TRANSPARENT',
    'RED',
    'GREEN',
    'BLUE',
    'WHITE',
    'BLACK',
]
