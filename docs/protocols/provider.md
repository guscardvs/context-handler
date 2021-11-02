# Provider Protocol

The Provider protocol is needed to add compatibility between
SyncContext and the client

## Signature

```Python

class MyProvider:

    state_name: str

    def is_closed(self, client: T) -> bool:
        """Returns if client is closed or released"""

    def close_client(self, client: T) -> None:
        """Closes/releases client"""

    def acquire(self) -> typing.ContextManager[T]:
        """Acquires a client `T` and releases at the end"""

```

## Methods

<details>
 <summary><code>def is_closed(self, client: ClientType) -> bool</code></summary>
Method to indicate if client is closed/released
</details>

<details>
 <summary><code>def close_client(self, client: ClientType) -> None</code></summary>
Method to close/release client
</details>

<details>
 <summary><code>def acquire(self) ->  typing.ContextManager[ClientType]</code></summary>
Method to acquire an open client and close it outside context
</details>
