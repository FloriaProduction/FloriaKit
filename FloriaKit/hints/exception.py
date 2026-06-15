import typing as t

type ExceptionOrStr = Exception | str


if t.TYPE_CHECKING:

    @t.overload
    def get_exception(
        exc: ExceptionOrStr,
        /,
        *,
        exc_class: t.Type[Exception] | None = None,
    ) -> Exception: ...

    @t.overload
    def get_exception[TD](
        exc: ExceptionOrStr | None,
        /,
        *,
        exc_class: t.Type[Exception] | None = None,
        default: TD = None,
    ) -> Exception | TD: ...


def get_exception(
    exc: ExceptionOrStr | None,
    *,
    exc_class: t.Type[Exception] | None = None,
    **kw: t.Any,
) -> t.Any:
    if exc is None:
        if 'default' in kw:
            return kw['default']

        raise ValueError()

    return (
        exc
        if isinstance(exc, Exception)
        else (Exception if exc_class is None else exc_class)(exc)
    )


__all__ = [
    'ExceptionOrStr',
    'get_exception',
]
