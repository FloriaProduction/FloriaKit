import typing as t

if t.TYPE_CHECKING:
    from .. import rgb

RED: 'rgb' = (255, 0, 0)
GREEN: 'rgb' = (0, 255, 0)
BLUE: 'rgb' = (0, 0, 255)

WHITE: 'rgb' = (255, 255, 255)
BLACK: 'rgb' = (0, 0, 0)

__all__ = [
    'RED',
    'GREEN',
    'BLUE',
    'WHITE',
    'BLACK',
]
