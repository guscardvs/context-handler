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
