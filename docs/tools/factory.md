# Context Factory

Context Factory can be used to handle contexts inside web applications
such as `FastAPI`/`Starlette` or `Sanic`.
It will create a context and register it to the request state
or get the context which is already in the request

## Usage

To use a request instance must have a state object such as:

- `.state` in `FastAPI`/`Starlette`
- `.ctx` in `Sanic`

### Sync

```Python
from context_handler.getters import context_factory

async def my_route(request: Request):
    factory = context_factory(MyProvider, SyncContext)
    context = factory(request)
```

### Async

```Python
from context_handler.getters import context_factory

async def my_route(request: Request):
    factory = context_factory(MyAsyncProvider, AsyncContext)
    context = factory(request)
```
