import typing

import sqlalchemy as sa
import sqlalchemy.engine as sa_engine
from lazyfields import lazyfield

from context_handler import interfaces
from context_handler.context import Context

TransactionOption = typing.Optional[typing.Literal['open', 'begin']]


class SaAdapter(interfaces.Adapter[sa_engine.Connection]):
    @typing.overload
    def __init__(
        self,
        *,
        uri: str,
        engine: None = None,
    ) -> None: ...

    @typing.overload
    def __init__(
        self,
        *,
        uri: None = None,
        engine: sa_engine.Engine,
    ) -> None: ...

    def __init__(
        self,
        *,
        uri: typing.Optional[str] = None,
        engine: typing.Optional[sa_engine.Engine] = None,
    ) -> None:
        if not any((uri, engine)):
            raise TypeError('Missing parameters (uri/engine)')
        self._uri = uri
        if engine is not None:
            self._engine = engine

    @lazyfield
    def _engine(self):
        assert self._uri
        return sa.create_engine(self._uri)

    def is_closed(self, client: sa_engine.Connection) -> bool:
        return client.closed

    def new(self):
        return self._engine.connect()

    def release(self, client: sa_engine.Connection) -> None:
        client.close()

    def context(self) -> 'Context[sa_engine.Connection]':
        return Context(self)
