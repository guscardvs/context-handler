# Context Handler

Context Handler is a library to reuse client/connection reuse
inside the same context/request/call.

## Installation

```console
pip install context-handler
```

## Example

### Create a provider

- Create a provider following the `_datastructures.Provider` Protocol

```python
class ConnectionProvider:
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
```

<details markdown="1">
<summary>Or use <code>_datastructures.AsyncProvider</code> protocol ...</summary>

If your code uses <code>async</code> / <code>await</code>, use <code>async def</code>:

```Python hl_lines="9  14"
class AsyncConnectionProvider:
    state_name = "connection_provider"

    def __init__(self):
        self.engine = create_engine("aiosqlite+sqlite://:memory:")

    @asynccontextmanager
    async def acquire(self):
        async with self.engine.connect() as conn:
            async with conn.begin():
                yield conn

    def is_closed(self, conn: Connection):
        return conn.closed

    async def close_client(self, conn: Connection):
        conn.close()
```

</details>

### Wrap your code

- Wrap a `function`

```Python hl_lines="9 14"
@ensure_context.sync_context
def make_some_query(context: SyncContext[Connection]):
    with context.begin() as client:
        client.execute(sql_stmt)
```

<details markdown="1">
<summary>Or use <code>async</code>...</summary>

```Python hl_lines="9 14"
@ensure_context.async_context
async def make_some_async_query(context: AsyncContext[Connection]):
    async with context.begin() as client:
        client.execute(sql_stmt)
```

</details>

### Create your context with a provider instance

- `sync`: `sync_context = SyncContext[Connection](ConnectionProvider())`
- `async`: `async_context = AsyncContext[Connection](ConnectionProvider())`

### Run inside the context manager

Every call `.begin()` inside the `.open()` context manager
will yield the same client instance, which can also be accessed from
`context.client` (**not recommended**)

```Python hl_lines="9 14"
with sync_context.open():
    with sync_context.begin() as client:
        client.execute(sql_stmt)
    make_some_query(sync_context), make_some_query(sync_context), make_some_query(sync_context)
```

<details markdown="1">
<summary>Or use <code>async</code>...</summary>

```Python hl_lines="9 14"
async def main():
    async with async_context.open():
        async with async_context.begin() as client:
            await client.execute(sql_stmt)
        await asyncio.gather(
            make_some_async_query(async_context),
            make_some_async_query(async_context),
            make_some_async_query(async_context)
        )
asyncio.run(main())
```

</details>
