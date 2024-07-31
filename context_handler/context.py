import asyncio
import contextlib
import threading
import typing

from lazyfields import asynclazyfield, dellazy, is_initialized, lazyfield

from context_handler import interfaces
from context_handler.typedef import AsyncT, T


class Context(typing.Generic[T]):
    def __init__(self, adapter: interfaces.Adapter[T]) -> None:
        self._adapter = adapter
        self._stack = 0
        self._lock = threading.Lock()

    @lazyfield
    def client(self) -> T:
        return self.adapter.new()

    @property
    def stack(self):
        return self._stack

    @property
    def adapter(self) -> interfaces.Adapter[T]:
        return self._adapter

    def is_active(self) -> bool:
        return self._stack > 0

    def acquire(self):
        with self._lock:
            if is_initialized(self, 'client') and self.adapter.is_closed(
                self.client
            ):
                dellazy(self, 'client')
            self._stack += 1
            return self.client

    def release(self):
        with self._lock:
            if self._stack == 1:
                self.adapter.release(self.client)
                dellazy(self, 'client')
            self._stack -= 1

    def __enter__(self) -> T:
        return self.acquire()

    def __exit__(self, *_) -> None:
        return self.release()

    @contextlib.contextmanager
    def open(self) -> typing.Generator[None, None, None]:
        with self:
            yield

    @contextlib.contextmanager
    def begin(self) -> typing.Generator[T, None, None]:
        with self as client:
            yield client


class AsyncContext(typing.Generic[AsyncT]):
    def __init__(self, adapter: interfaces.AsyncAdapter[AsyncT]) -> None:
        self._adapter = adapter
        self._stack = 0
        self._lock = asyncio.Lock()

    @property
    def stack(self) -> int:
        """Returns how many frames are using this context"""
        return self._stack

    @property
    def adapter(self) -> interfaces.AsyncAdapter[AsyncT]:
        return self._adapter

    def is_active(self) -> bool:
        return self._stack > 0

    @asynclazyfield
    async def client(self) -> AsyncT:
        return await self.adapter.new()

    async def acquire(self):
        async with self._lock:
            client = await self.client()
            self._stack += 1
            return client

    async def release(self):
        async with self._lock:
            if self._stack == 1:
                client = await self.client()
                await self.adapter.release(client)
                dellazy(self, 'client')
            self._stack -= 1

    async def __aenter__(self) -> AsyncT:
        return await self.acquire()

    async def __aexit__(self, *_) -> None:
        await self.release()

    @contextlib.asynccontextmanager
    async def open(self) -> typing.AsyncGenerator[None, None]:
        async with self:
            yield

    @contextlib.asynccontextmanager
    async def begin(self) -> typing.AsyncGenerator[AsyncT, None]:
        async with self as client:
            yield client
