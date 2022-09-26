import contextlib
import typing

import sqlalchemy as sa
import sqlalchemy.engine as sa_engine
import sqlalchemy.orm as sa_orm

from context_handler import context
from context_handler import interfaces
from context_handler.utils import lazy


class SaAdapter(interfaces.Adapter[sa_engine.Connection]):
    @typing.overload
    def __init__(
        self,
        *,
        uri: str,
        engine: None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        *,
        uri: None = None,
        engine: sa_engine.Engine,
    ) -> None:
        ...

    def __init__(
        self,
        *,
        uri: str | None = None,
        engine: sa_engine.Engine | None = None,
    ) -> None:
        if not any((uri, engine)):
            raise TypeError('Missing parameters (uri/engine)')
        self._uri = uri
        if engine is not None:
            self._engine = engine

    @lazy.lazy_property
    def _engine(self):
        assert self._uri
        return sa.create_engine(self._uri)

    def is_closed(self, client: sa_engine.Connection) -> bool:
        return client.closed

    def new(self):
        return self._engine.connect()

    def release(self, client: sa_engine.Connection) -> None:
        client.close()


class SaContext(context.Context[sa_engine.Connection]):
    def __init__(
        self,
        adapter: interfaces.Adapter[sa_engine.Connection],
        transaction_on: typing.Literal['open', 'begin'] | None = 'open',
    ) -> None:
        super().__init__(adapter)
        self._transaction_on = transaction_on

    def _make_transaction(self, connection: sa_engine.Connection):
        if self._transaction_on is None:
            return contextlib.nullcontext()
        if connection.in_transaction():
            return typing.cast(
                typing.ContextManager, connection.begin_nested()
            )
        return connection.begin()

    def open(self):
        if self._transaction_on != 'open':
            return super().open()
        return self._transaction_open()

    def begin(self):
        if self._transaction_on != 'begin':
            return super().begin()
        return self._transaction_begin()

    @lazy.lazy_property
    def client(self):
        return self.adapter.new()

    @contextlib.contextmanager
    def _transaction_open(self):
        with super().open():
            with self._make_transaction(self.client):
                yield

    @contextlib.contextmanager
    def transaction_begin(self):
        with super().begin() as client:
            with self._make_transaction(client):
                yield client

    @contextlib.contextmanager
    def acquire_session(
        self,
    ):
        with self.begin() as conn:
            with sa_orm.Session(conn) as session:
                yield session
