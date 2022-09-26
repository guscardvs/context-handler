import typing

from context_handler import context
from context_handler import interfaces
from context_handler.typedef import AsyncT
from context_handler.typedef import T
from context_handler.utils import lazy


class _FactoryWrapper(typing.Generic[T]):
    def __init__(self, adapter: interfaces.Adapter[T]) -> None:
        self._adapter = adapter

    def __call__(self) -> interfaces.Handler[T]:
        return self.context

    def get(self):
        return context.Context(self._adapter)

    @lazy.lazy_property
    def context(self):
        return self.get()

    def begin(self):
        return self.context.begin()

    def open(self):
        return self.context.open()

    def is_active(self):
        return self.context.is_active()


class _AsyncFactoryWrapper(typing.Generic[AsyncT]):
    def __init__(self, adapter: interfaces.AsyncAdapter[AsyncT]) -> None:
        self._adapter = adapter

    def __call__(self) -> interfaces.AsyncHandler[AsyncT]:
        return self.context

    def get(self):
        return context.AsyncContext(self._adapter)

    @lazy.lazy_property
    def context(self):
        return self.get()

    def begin(self):
        return self.context.begin()

    def open(self):
        return self.context.open()

    def is_active(self):
        return self.context.is_active()


def async_context_factory(
    adapter: interfaces.AsyncAdapter[AsyncT],
) -> _AsyncFactoryWrapper[AsyncT]:
    return _AsyncFactoryWrapper(adapter)


def context_factory(
    adapter: interfaces.Adapter[T],
) -> _FactoryWrapper[T]:
    return _FactoryWrapper(adapter)
