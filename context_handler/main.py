import typing

from context_handler import context
from context_handler import interfaces
from context_handler.typedef import AsyncT
from context_handler.typedef import T


def async_context_factory(
    adapter: interfaces.AsyncAdapter[AsyncT],
) -> typing.Callable[[], interfaces.AsyncHandler[AsyncT]]:
    def _get_context():
        return context.AsyncContext(adapter)

    return _get_context


def context_factory(
    adapter: interfaces.Adapter[T],
) -> typing.Callable[[], interfaces.Handler[T]]:
    def _get_context():
        return context.Context(adapter)

    return _get_context
