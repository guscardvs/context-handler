import typing

import aiohttp

from context_handler import interfaces


def _default_factory(client_args: typing.Mapping[str, typing.Any]):
    def _factory():
        return aiohttp.ClientSession(**client_args)

    return _factory


class AsyncHttpAdapter(interfaces.AsyncAdapter[aiohttp.ClientSession]):
    def __init__(
        self,
        client_factory: typing.Callable[[], aiohttp.ClientSession]
        | None = None,
        **client_session_args: typing.Any
    ) -> None:
        self._client_factory = client_factory or _default_factory(
            client_session_args
        )

    def is_closed(self, client: aiohttp.ClientSession) -> bool:
        return client.closed

    async def release(self, client: aiohttp.ClientSession) -> None:
        return await client.close()

    async def new(self):
        return self._client_factory()
