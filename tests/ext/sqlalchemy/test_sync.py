import sqlalchemy as sa

import context_handler
from context_handler.ext import sqlalchemy

sqlite_uri = 'sqlite:///:memory:'


def test_sqlalchemy_adapter_works_correctly_with_default_context():
    adapter = sqlalchemy.SaAdapter(uri=sqlite_uri)
    factory = context_handler.context_factory(adapter)

    with factory.begin() as conn:
        result = conn.execute('SELECT 1').first()
        assert result
        (first,) = result
        assert first == 1


def test_sqlalchemy_adapter_works_correctly_with_sa_context():
    adapter = sqlalchemy.SaAdapter(uri=sqlite_uri)

    factory = adapter.context()

    with factory.begin() as conn:
        result = conn.execute('SELECT 1').first()
        assert result
        (first,) = result
        assert first == 1


def test_sqlalchemy_adapter_works_correctly_with_sa_context_transaction():
    adapter = sqlalchemy.SaAdapter(uri=sqlite_uri)
    factory = adapter.context(transaction_on='begin')
    with factory.open():
        with factory.begin() as conn:
            result = conn.execute('SELECT 1').first()
            assert result
            assert conn.in_transaction()
            assert not conn.in_nested_transaction()
            (first,) = result
            assert first == 1

    factory = adapter.context(transaction_on='open')

    with factory.open():
        with factory.begin():
            assert factory.client.in_transaction()
            assert not factory.client.in_nested_transaction()


def test_sqlalchemy_adapter_works_correctly_with_sa_acquire_session():
    adapter = sqlalchemy.SaAdapter(uri=sqlite_uri)
    factory = adapter.context()

    with factory.acquire_session() as session:
        result = session.execute(sa.text('SELECT 1')).first()
        assert result
        (first,) = result
        assert first == 1
