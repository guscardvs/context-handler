import typing

from lazyfields import lazyfield

from context_handler import context, interfaces
from context_handler.typedef import AsyncT, T


class _FactoryWrapper(typing.Generic[T]):
    def __init__(self, adapter: interfaces.Adapter[T]) -> None:
        self._adapter = adapter

    def __call__(self) -> context.Context[T]:
        return self.context

    def get(self):
        return context.Context(self._adapter)

    @lazyfield
    def context(self):
        return self.get()

    def __enter__(self):
        return self.context.__enter__()

    def __exit__(self, *exc):
        return self.context.__exit__(*exc)

    def begin(self):
        return self.context.begin()

    def open(self):
        return self.context.open()

    def is_active(self):
        return self.context.is_active()


class _AsyncFactoryWrapper(typing.Generic[AsyncT]):
    def __init__(self, adapter: interfaces.AsyncAdapter[AsyncT]) -> None:
        self._adapter = adapter

    def __call__(self) -> context.AsyncContext[AsyncT]:
        return self.context

    def get(self):
        return context.AsyncContext(self._adapter)

    @lazyfield
    def context(self):
        return self.get()

    async def __aenter__(self):
        return await self.context.__aenter__()

    async def __aexit__(self, *exc):
        return await self.context.__aexit__(*exc)

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
