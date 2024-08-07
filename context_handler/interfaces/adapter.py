import typing

from context_handler.typedef import AsyncT, T


class Adapter(typing.Protocol[T]):
    def is_closed(self, client: T) -> bool:
        """Returns if client state is closed or released"""
        ...

    def release(self, client: T) -> None:
        """Closes or releases client"""
        ...

    def new(self) -> T:
        """Creates new client"""
        ...


class AsyncAdapter(typing.Protocol[AsyncT]):
    async def is_closed(self, client: AsyncT) -> bool:
        """Returns if client state is closed or released"""
        ...

    async def release(self, client: AsyncT) -> None:
        """Closes or releases client"""
        ...

    async def new(self) -> AsyncT:
        """Creates new client"""
        ...
