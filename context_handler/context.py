import typing
from contextlib import asynccontextmanager, contextmanager

from context_handler import _datastructures, exc

T = typing.TypeVar("T")


class SyncContext(typing.Generic[T]):
    def __init__(self, provider: _datastructures.Provider[T]) -> None:
        self._provider = provider
        self._inside_ctx = False
        self._client: typing.Optional[T] = None

    def in_context(self):
        if self._client is None:
            return False
        return not self._provider.is_closed(self._client)

    @property
    def client(self) -> T:
        if self._client is None:
            raise exc.ContextNotInitializedError
        return self._client

    def _set_client(self, client: T):
        self._client = client

    def _reset_context(self):
        if self._client is None:
            return
        if not self._provider.is_closed(self._client):
            self._provider.close_client(self._client)
        self._client = None
        self._inside_ctx = False

    def _open_context(self):
        with self._provider.acquire() as client:
            self._client = client
            self._inside_ctx = True
            yield
        self._reset_context()

    def _begin_context(self):
        with self._provider.acquire() as client:
            yield client

    def _contexted_begin(self):
        yield self._client

    def _contexted_open(self):
        yield

    @contextmanager
    def begin(self):
        if self.in_context():
            return self._contexted_begin()
        return self._begin_context()

    @contextmanager
    def open(self):
        if self.in_context():
            return self._contexted_open()
        return self._open_context()


class AsyncContext(typing.Generic[T]):
    def __init__(self, provider: _datastructures.AsyncProvider[T]) -> None:
        self._provider = provider
        self._inside_ctx = False
        self._client: typing.Optional[T] = None

    def in_context(self):
        if self._client is None:
            return False
        return not self._provider.is_closed(self._client)

    @property
    def client(self) -> T:
        if self._client is None:
            raise exc.ContextNotInitializedError
        return self._client

    def _set_client(self, client: T):
        self._client = client

    async def _reset_context(self):
        if self._client is None:
            return
        if not self._provider.is_closed(self._client):
            await self._provider.close_client(self._client)
        self._client = None
        self._inside_ctx = False

    async def _open_context(self):
        async with self._provider.acquire() as client:
            self._client = client
            self._inside_ctx = True
            yield
        await self._reset_context()

    async def _begin_context(self):
        async with self._provider.acquire() as client:
            yield client

    async def _contexted_begin(self):
        yield self._client

    async def _contexted_open(self):
        yield

    @asynccontextmanager
    def begin(self):
        if self.in_context():
            return self._contexted_begin()
        return self._begin_context()

    @asynccontextmanager
    def open(self):
        if self.in_context():
            return self._contexted_open()
        return self._open_context()
