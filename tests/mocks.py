import context_handler


class MockClient:
    def __init__(self) -> None:
        self._active = True

    def toggle_active(self):
        self._active = not self._active

    def deactivate(self):
        self._active = False

    @property
    def closed(self):
        return not self._active

    def __enter__(self):
        self.toggle_active()
        return self

    def __exit__(self, *_):
        self.toggle_active()

    async def __aenter__(self):
        self.toggle_active()
        return self

    async def __aexit__(self, *_):
        self.toggle_active()


class MockAdapter(context_handler.Adapter[MockClient]):
    def is_closed(self, client: MockClient) -> bool:
        return client.closed

    def release(self, client: MockClient) -> None:
        return client.deactivate()

    def new(self) -> MockClient:
        return MockClient()


class MockAsyncAdapter(context_handler.AsyncAdapter[MockClient]):
    async def is_closed(self, client: MockClient) -> bool:
        return client.closed

    async def release(self, client: MockClient) -> None:
        client.deactivate()

    async def new(self) -> MockClient:
        return MockClient()
