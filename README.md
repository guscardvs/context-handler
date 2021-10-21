# Context Handler
Context handler to ensure complete lifecycle to a client

## Usage:
- Example with sqlalchemy.Connection
```python
from context_handler import SyncContext
from contextlib import contextmanager
from sqlalchemy.engine import Connection


class ConnectionProvider:
    """ConnectionProvider must follow Provider Protocol from ._datastructures.Provider"""
    
    state_name = "connection_provider"

    def __init__(self):
        self.engine = create_engine("sqlite://:memory:")

    @contextmanager
    def acquire(self):
        with self.engine.connect() as conn:
            with conn.begin():
                yield conn

    def is_closed(self, conn: Connection):
        return conn.closed

    def close_client(self, conn: Connection):
        conn.close()


context = SyncContext[Connection](ConnectionProvider())
with context.open():
    with context.begin() as client:  # client here is a sqlalchemy.Connection instance
        client.execute(sql_stmt)
    with context.begin() as client:  # client here is the same instance from the last .begin() call
        client.execute(sql_stmt)
# outside .open(), sqlalchemy.Connection is no longer available
```
- Exeample with aiohttp.ClientSession
```python
from context_handler import AsyncContext
from contextlib import asynccontextmanager
import aiohttp
import asyncio


class ClientSessionProvider:
    """ClientSessionProvider must follow AsyncProvider Protocol from ._datastructures.AsyncProvider"""
    
    state_name = "client_session_provider"

    @asynccontextmanager
    async def acquire(self):
        async with aiohttp.ClientSession() as session:
            yield session

    def is_closed(self, client: aiohttp.ClientSession):
        return client.closed

    async def close_client(self, client: aiohttp.ClientSession):
        await client.close()


async def run():
    context = AsyncContext[aiohttp.ClientSession](ClientSessionProvider())
    async with context.open():
        async with context.begin() as client:  # client here is an aiohttp.ClientSession instance
            async with client.get(some_route) as response:
                ...
        with context.begin() as client:  # client here is the same instance from the last .begin() call
            async with client.get(some_route) as response:
                ...


asyncio.run(run())
# outside .open(), the aiohttp.ClientSession instance is no longer available
```
