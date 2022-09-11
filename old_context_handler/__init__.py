__version__ = '4.0.2'
__version_info__ = tuple(
    map(
        lambda val: int(val) if val.isnumeric() else val,
        __version__.split('.'),
    )
)

from . import ensure_context
from . import exc
from ._datastructures import ImmutableAsyncProvider
from ._datastructures import ImmutableSyncProvider
from ._datastructures import StateWrapper
from .context import AsyncContext
from .context import SyncContext
from .generic import AsyncGenericFactory
from .generic import GenericFactory
from .getters import ArgType
from .getters import context_factory
from .getters import get_context
from .parent import context_class

__all__ = [
    'AsyncContext',
    'SyncContext',
    'context_factory',
    'get_context',
    'GenericFactory',
    'AsyncGenericFactory',
    'exc',
    'ensure_context',
    'ArgType',
    'ImmutableSyncProvider',
    'ImmutableAsyncProvider',
    'StateWrapper',
    'context_class',
]
