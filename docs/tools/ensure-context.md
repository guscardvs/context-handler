# Ensure Context

The ensure context utility is used to ensure an open context inside a function
consuming the context from the parameters

## Usage

### Function

```Python
from context_handler import ensure_context


@ensure_context.sync_context
def make_some_query(context: SyncContext[Connection]):
    with context.begin() as client:
        client.execute(sql_stmt)
```

### Instance

```Python
from context_handler import ensure_context


class MyClass:
    def __init__(self, context: SyncContext):
        self._context = context

    @ensure_context.sync_context(
        first_arg_type="instance",
        context_attr_name="_context",
    )
    def make_some_query(self):
        with self._context.begin() as client:
            client.execute(sql_stmt)
```

### View

```Python
from context_handler import ensure_context, context_factory


factory = context_factory(provider.MyProvider, SyncContext)

@ensure_context.sync_context(
    first_arg_type="view",
    _factory=factory
)
async def my_route(request: Request):
    with factory(request).begin() as client:
        client.execute(sql_stmt)

```

### Obs: AsyncContext

To use an AsyncContext just change

- from:
  `ensure_context.sync_context`
- to
  `ensure_context.async_context`
