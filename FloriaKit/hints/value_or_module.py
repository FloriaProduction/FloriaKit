import typing as t
import types as ts

from . import exception

type ValueOrModule[T] = T | ts.ModuleType

if t.TYPE_CHECKING:

    @t.overload
    def get_from_module[T](
        value_or_module: ValueOrModule[T],
        name: str,
        /,
    ) -> T: ...

    @t.overload
    def get_from_module[T](
        value_or_module: ValueOrModule[T],
        name: str,
        /,
        *,
        exception: exception.ExceptionOrStr,
    ) -> T: ...

    @t.overload
    def get_from_module[T, TD](
        value_or_module: ValueOrModule[T],
        name: str,
        /,
        *,
        default: TD,
    ) -> T | TD: ...


def get_from_module(
    value_or_module: ValueOrModule[t.Any],
    name: str,
    **kw: t.Any,
) -> t.Any:
    if isinstance(value_or_module, ts.ModuleType):
        if not hasattr(value_or_module, name):
            if 'default' in kw:
                return kw['default']
            raise exception.get_exception(
                kw.get('exception'),
                default=ValueError(
                    f'Variable with name "{name}" not found in module: {value_or_module}'
                ),
            )

        return getattr(value_or_module, name)

    return value_or_module


__all__ = [
    'ValueOrModule',
    'get_from_module',
]
