__version__ = "1.1.0"
__version_info__ = tuple(
    map(
        lambda val: int(val) if val.isnumeric() else val,
        __version__.split("."),
    )
)

from . import exc
from ._datastructures import (
    ContextGetter,
    ImmutableAsyncProvider,
    ImmutableSyncProvider,
    StateWrapper,
)
from .context import AsyncContext, SyncContext
from . import ensure_context
from .factory import context_factory

__all__ = [
    "AsyncContext",
    "SyncContext",
    "context_factory",
    "exc",
    "ensure_context",
    "ContextGetter",
    "ImmutableSyncProvider",
    "ImmutableAsyncProvider",
    "StateWrapper",
]
