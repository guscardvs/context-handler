import context_handler
from context_handler import context
from tests import mocks


def test_context_factory_returns_valid_context_on_call():
    factory = context_handler.context_factory(mocks.MockAdapter())
    with factory.begin() as client:
        assert factory.is_active()
        assert isinstance(factory.context, context.Context)

    assert client.closed


async def test_async_context_factory_return_valid_async_context_on_call():
    factory = context_handler.async_context_factory(mocks.MockAsyncAdapter())
    async with factory.begin() as client:
        assert factory.is_active()
        assert isinstance(factory.context, context.AsyncContext)

    assert client.closed
