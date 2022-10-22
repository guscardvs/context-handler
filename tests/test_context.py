import contextlib

import context_handler
from context_handler import context
from tests import mocks


class CustomException(Exception):
    pass


def test_context_factory_returns_valid_context_on_call():
    factory = context_handler.context_factory(mocks.MockAdapter())
    with factory.open():
        with factory.begin() as client:
            assert factory.is_active()
            assert isinstance(factory.context, context.Context)

    assert client.closed
    assert factory.context.stack == 0


async def test_async_context_factory_return_valid_async_context_on_call():
    factory = context_handler.async_context_factory(mocks.MockAsyncAdapter())
    async with factory.open():
        async with factory.begin() as client:
            assert factory.is_active()
            assert isinstance(factory.context, context.AsyncContext)

    assert client.closed
    assert factory.context._client is None
    assert factory.context.stack == 0


def test_context_closes_correctly_when_exception_raised_on_open():
    factory = context_handler.context_factory(mocks.MockAdapter())
    with contextlib.suppress(CustomException):
        with factory.open():
            client = factory.context.client
            raise CustomException()

    assert client.closed   # type: ignore
    assert factory.context.stack == 0


def test_context_closes_correctly_when_exception_raised_on_begin():
    factory = context_handler.context_factory(mocks.MockAdapter())
    with contextlib.suppress(CustomException):
        with factory.begin() as client:
            raise CustomException()

    assert client.closed  # type: ignore
    assert factory.context.stack == 0


async def test_asynccontext_closes_correctly_when_exception_raised_on_open():
    factory = context_handler.async_context_factory(mocks.MockAsyncAdapter())
    with contextlib.suppress(CustomException):
        async with factory.open():
            raise CustomException()

    assert factory.context._client is None
    assert factory.context.stack == 0


async def test_asynccontext_closes_correctly_when_exception_raised_on_begin():
    factory = context_handler.async_context_factory(mocks.MockAsyncAdapter())
    with contextlib.suppress(CustomException):
        async with factory.begin():
            raise CustomException()

    assert factory.context._client is None
    assert factory.context.stack == 0
