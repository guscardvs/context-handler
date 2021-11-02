# Generic Factory

Generic Factory can be used to handle contexts inside web applications
such as `FastAPI`/`Starlette` or `Sanic`.
Differently than a regular context factory it can be used
with the `typing.Generic` annotation

## Usage

To use a request instance must have a state object such as:

- `.state` in `FastAPI`/`Starlette`
- `.ctx` in `Sanic`

### Sync

```Python
from context_handler.getters import GenericFactory

async def my_route(request: Request):
    factory = GenericFactory[MyProvider, MyClient](request)
    context = factory.get()
```

### Async

```Python
from context_handler.getters import AsyncGenericFactory

async def my_route(request: Request):
    factory = GenericFactory[MyAsyncProvider, MyClient](request)
    context = factory.get()
```

## FastAPI (Not Tested Yet)

Generic Factory can also be used with the `fastapi.Depends()`
utility provided by FastAPI

```Python
from context_handler.getters import AsyncGenericFactory
from fastapi import Depends

async def my_route(factory: GenericFactory[MyAsyncProvider, MyClient] = Depends()):
    context = factory.get()
```
