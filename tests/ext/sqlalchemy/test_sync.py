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
