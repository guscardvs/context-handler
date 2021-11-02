# AsyncProvider Protocol

The AsyncProvider protocol is needed to add compatibility between
SyncContext and the client

## Signature

```Python

class MyAsyncProvider:

    state_name: str

    def is_closed(self, client: T) -> bool:
        """Returns if client is closed or released"""

    async def close_client(self, client: T) -> None:
        """Closes/releases client"""

    async def acquire(self) -> typing.ContextManager[T]:
        """Acquires a client `T` and releases at the end"""

```

## Methods

<details>
 <summary><code>def is_closed(self, client: ClientType) -> bool</code></summary>
Method to indicate if client is closed/released
</details>

<details>
 <summary><code>async def close_client(self, client: ClientType) -> None</code></summary>
Method to close/release client
</details>

<details>
 <summary><code>async def acquire(self) ->  typing.AsyncContextManager[ClientType]</code></summary>
Method to acquire an open client and close it outside context
</details>
