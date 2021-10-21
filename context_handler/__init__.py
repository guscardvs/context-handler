__version__ = "0.1.0"
__version_info__ = tuple(
    map(lambda val: int(val) if val.isnumeric() else val, __version__.split("."))
)

from . import exc
from .context import AsyncContext, SyncContext
from .factory import get_factory
from .utils import ensure_context

__all__ = ["AsyncContext", "SyncContext", "get_factory", "exc", "ensure_context"]
