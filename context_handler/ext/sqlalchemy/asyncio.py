import typing

import sqlalchemy.ext.asyncio as sa_asyncio
from lazyfields import lazyfield

from context_handler import interfaces
from context_handler.context import AsyncContext

TransactionOptions = typing.Optional[typing.Literal['open', 'begin']]


class AsyncSaAdapter(interfaces.AsyncAdapter[sa_asyncio.AsyncConnection]):
    @typing.overload
    def __init__(
        self,
        *,
        uri: str,
        engine: None = None,
    ) -> None: ...

    @typing.overload
    def __init__(
        self,
        *,
        uri: None = None,
        engine: sa_asyncio.AsyncEngine,
    ) -> None: ...

    def __init__(
        self,
        *,
        uri: typing.Optional[str] = None,
        engine: typing.Optional[sa_asyncio.AsyncEngine] = None,
    ) -> None:
        if not any((uri, engine)):
            raise TypeError('Missing parameters (uri/engine)')
        self._uri = uri
        if engine is not None:
            self._engine = engine

    @lazyfield
    def _engine(self):
        assert self._uri
        return sa_asyncio.create_async_engine(self._uri)

    def _create_connection(self):
        return self._engine.connect()

    async def is_closed(self, client: sa_asyncio.AsyncConnection) -> bool:
        return client.closed

    async def release(self, client: sa_asyncio.AsyncConnection) -> None:
        return await client.close()

    async def new(self) -> sa_asyncio.AsyncConnection:
        return await self._create_connection()

    def context(self) -> 'AsyncContext[sa_asyncio.AsyncConnection]':
        return AsyncContext(self)
