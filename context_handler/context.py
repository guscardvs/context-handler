import contextlib

from context_handler import interfaces
from context_handler.typedef import AsyncT
from context_handler.typedef import T
from context_handler.utils import lazy


class Context(interfaces.Handler[T]):
    def __init__(self, adapter: interfaces.Adapter[T]) -> None:
        self._adapter = adapter
        self._stack = 0

    @lazy.lazy_property
    def client(self) -> T:
        return self.adapter.new()

    @property
    def adapter(self) -> interfaces.Adapter[T]:
        return self._adapter

    def is_active(self) -> bool:
        return self._stack > 0

    def acquire(self):
        if self.adapter.is_closed(self.client):
            del self.client
        self._stack += 1
        return self.client

    def release(self):
        if self._stack == 1:
            self.adapter.release(self.client)
            del self.client
        self._stack -= 1

    @contextlib.contextmanager
    def open(self):
        self.acquire()
        yield
        self.release()

    @contextlib.contextmanager
    def begin(self):
        yield self.acquire()
        self.release()


class AsyncContext(interfaces.AsyncHandler[AsyncT]):
    def __init__(self, adapter: interfaces.AsyncAdapter[AsyncT]) -> None:
        self._adapter = adapter
        self._stack = 0
        self._client: AsyncT | None = None

    @property
    def adapter(self) -> interfaces.AsyncAdapter[AsyncT]:
        return self._adapter

    def is_active(self) -> bool:
        return self._stack > 0

    async def client(self) -> AsyncT:
        if self._client is None or await self._adapter.is_closed(self._client):
            self._client = await self._adapter.new()
        return self._client

    async def acquire(self):
        client = await self.client()
        self._stack += 1
        return client

    async def release(self):
        if self._client is None:
            raise RuntimeError(
                'Release should not be called before client initialization'
            )
        if self._stack == 1:
            await self.adapter.release(self._client)
            self._client = None
        self._stack -= 1

    @contextlib.asynccontextmanager
    async def open(self):
        await self.acquire()
        yield
        await self.release()

    @contextlib.asynccontextmanager
    async def begin(self):
        yield await self.acquire()
        await self.release()
