import typing
import warnings
from functools import wraps

P = typing.ParamSpec('P')
T = typing.TypeVar('T')


def no_cover(func: typing.Callable[P, T]) -> typing.Callable[P, T]:
    return func


@no_cover
def deprecated(func: typing.Callable[P, T]) -> typing.Callable[P, T]:
    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        warnings.warn(
            f'Function {func.__qualname__} is '
            'deprecated and can be removed without notice',
            DeprecationWarning,
        )
        return func(*args, **kwargs)

    return inner
