import typing as t

from .. import hints

if t.TYPE_CHECKING:

    @t.overload
    def not_none[T](
        value: T | None,
        *,
        exception: hints.ExceptionOrStr | None = None,
    ) -> T: ...

    @t.overload
    def not_none[T, TD](
        value: T | None,
        *,
        default: TD = None,
    ) -> T | TD: ...


def raiser(exc: hints.ExceptionOrStr) -> t.NoReturn:
    raise hints.exception.get_exception(exc)


def not_none(value: t.Any, **kw: t.Any):
    if value is not None:
        return value

    if 'default' in kw:
        return kw['default']

    raise hints.get_exception(
        kw.get('exception'),
        default=ValueError('Value is None'),
    )


if t.TYPE_CHECKING:

    @t.overload
    def is_instance[T](
        value: t.Any,
        type_: t.Type[T],
        *,
        exception: hints.ExceptionOrStr | None = None,
    ) -> T: ...

    @t.overload
    def is_instance[T, TD](
        value: t.Any,
        type_: t.Type[T],
        *,
        default: TD = None,
    ) -> T | TD: ...


def is_instance(value: t.Any, type_: t.Type[t.Any], **kw: t.Any):
    if isinstance(value, type_):
        return value

    if 'default' in kw:
        return kw['default']

    raise hints.get_exception(
        kw.get('exception'),
        default=ValueError(f'Value is not instance of {type_.__name__}'),
    )


__all__ = [
    'raiser',
    'not_none',
    'is_instance',
]
