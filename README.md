# Context Handler

Context handler to ensure complete lifecycle to a client

## Usage

- Example with sqlalchemy.Connection

```python
from context_handler import SyncContext, ensure_context
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

@ensure_context.function # Utility to open context automatically before calling function
def make_some_query(context: SyncContext[Connection]):
    with context.begin() as client:  # client here is the same instance from the last .begin() call
        client.execute(sql_stmt)

context = SyncContext[Connection](ConnectionProvider())
with context.open():
    with context.begin() as client:  # client here is a sqlalchemy.Connection instance
        client.execute(sql_stmt)
    make_some_query(context), make_some_query(context), make_some_query(context)  # client inside these functions is the same instance from the last .begin() call

# outside .open(), sqlalchemy.Connection is no longer available
```

- Exeample with aiohttp.ClientSession

```python
from context_handler import AsyncContext, ensure_context
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

@ensure_context.awaitable # Utility to open context automatically before calling awaitable function
async def run_some_request(context: AsyncContext[aiohttp.ClientSession]):
    with context.begin() as client:
        async with client.get(some_route) as response:
            ...


async def run():
    context = AsyncContext[aiohttp.ClientSession](ClientSessionProvider())
    async with context.open():
        async with context.begin() as client:  # client here is an aiohttp.ClientSession instance
            async with client.get(some_route) as response:
                ...
        await asyncio.gather( run_some_request(context),  run_some_request(context),  run_some_request(context), )  # client inside these functions is the same instance from the last .begin() call



asyncio.run(run())
# outside .open(), the aiohttp.ClientSession instance is no longer available
```
