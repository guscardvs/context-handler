import sqlalchemy as sa

import context_handler
from context_handler.ext import sqlalchemy

sqlite_uri = 'sqlite+aiosqlite:///:memory:'


async def test_sqlalchemy_async_adapter_works_correctly_with_default_context():
    adapter = sqlalchemy.AsyncSaAdapter(uri=sqlite_uri)
    factory = context_handler.async_context_factory(adapter)

    async with factory.begin() as conn:
        result = await conn.execute(sa.text('SELECT 1'))
        response = result.first()
        assert response
        (first,) = response
        assert first == 1


async def test_sqlalchemy_async_adapter_works_correctly_with_sa_context():
    adapter = sqlalchemy.AsyncSaAdapter(uri=sqlite_uri)
    factory = adapter.context()

    async with factory.begin() as conn:
        result = await conn.execute(sa.text('SELECT 1'))
        response = result.first()
        assert response
        (first,) = response
        assert first == 1


async def test_sqlalchemy_async_adapter_works_correctly_with_sa_context_transaction():   # noqa
    adapter = sqlalchemy.AsyncSaAdapter(uri=sqlite_uri)
    factory = adapter.context(transaction_on='begin')

    async with factory.open():
        async with factory.begin() as conn:
            result = await conn.execute(sa.text('SELECT 1'))
            response = result.first()
            assert response
            assert conn.in_transaction()
            assert not conn.in_nested_transaction()
            (first,) = response
            assert first == 1

    factory = adapter.context(transaction_on='open')
    async with factory.open():
        async with factory.begin() as conn:
            assert conn.in_transaction()
            assert not conn.in_nested_transaction()


async def test_sqlalchemy_async_adapter_works_correctly_with_sa_acquire_session():   # noqa
    adapter = sqlalchemy.AsyncSaAdapter(uri=sqlite_uri)
    factory = adapter.context()

    async with factory.acquire_session() as session:
        result = await session.execute(sa.text('SELECT 1'))
        response = result.first()
        assert response
        (first,) = response
        assert first == 1
