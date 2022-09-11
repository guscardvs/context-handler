import contextlib
import typing

import sqlalchemy.ext.asyncio as sa_asyncio
from sqlalchemy.engine import URL

from context_handler import context
from context_handler import interfaces
from context_handler.utils import lazy


class AsyncSaAdapter(interfaces.AsyncAdapter[sa_asyncio.AsyncConnection]):
    def __init__(
        self,
        uri: URL | None = None,
        engine: sa_asyncio.AsyncEngine | None = None,
    ) -> None:
        if not any((uri, engine)):
            raise TypeError('Missing parameters (uri/engine)')
        self._uri = uri
        if engine is not None:
            self._engine = engine

    @lazy.lazy_property
    def _engine(self):
        return sa_asyncio.create_async_engine(self._uri)

    async def _create_connection(self):
        return self._engine.connect()

    def is_closed(self, client: sa_asyncio.AsyncConnection) -> bool:
        return client.closed

    async def release(self, client: sa_asyncio.AsyncConnection) -> None:
        return await client.close()

    async def new(self) -> sa_asyncio.AsyncConnection:
        return await self._create_connection()


class AsyncSaContext(context.AsyncContext[sa_asyncio.AsyncConnection]):
    def __init__(
        self,
        adapter: interfaces.AsyncAdapter[sa_asyncio.AsyncConnection],
        transaction_on: typing.Literal['open', 'begin'] | None = 'open',
    ) -> None:
        super().__init__(adapter)
        self._transaction_on = transaction_on

    def _make_transaction(self, connection: sa_asyncio.AsyncConnection):
        if self._transaction_on is None:
            return contextlib.nullcontext()
        if connection.in_transaction():
            return connection.begin_nested()
        return connection.begin()

    def open(self):
        if self._transaction_on != 'open':
            return super().open()
        return self._transaction_open()

    def begin(self):
        if self._transaction_on != 'begin':
            return super().begin()
        return self._transaction_begin()

    @contextlib.asynccontextmanager
    async def _transaction_open(self):
        async with super().open():
            async with self._make_transaction(await self.client()):
                yield

    @contextlib.asynccontextmanager
    async def _transaction_begin(self):
        async with super().begin() as client:
            async with self._make_transaction(client):
                yield client

    @contextlib.asynccontextmanager
    async def acquire_session(
        self,
    ) -> typing.AsyncGenerator[sa_asyncio.AsyncSession, None]:
        async with self.begin() as client:
            async with sa_asyncio.AsyncSession(client) as session:
                yield session
