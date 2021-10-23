import typing

T = typing.TypeVar("T")


@typing.runtime_checkable
class Provider(typing.Protocol[T]):
    """Client Adapter Interface Accepted by SyncContext"""

    state_name: str

    def is_closed(self, client: T) -> bool:
        """Returns if client is closed or released"""

    def close_client(self, client: T) -> None:
        """Closes/releases client"""

    def acquire(self) -> typing.ContextManager[T]:
        """Acquires a client `T` and releases at the end"""


@typing.runtime_checkable
class AsyncProvider(typing.Protocol[T]):
    """Client Adapter Interface Accepted by AsyncContext"""

    state_name: str

    def is_closed(self, client: T) -> bool:
        """Returns if client is closed or released"""

    async def close_client(self, client: T) -> None:
        """Closes/releases client"""

    def acquire(self) -> typing.AsyncContextManager[T]:
        """Acquires a client `T` and releases at the end"""


@typing.runtime_checkable
class AbstractSyncContext(typing.Protocol[T]):
    provider: Provider[T]
    inside_ctx: bool

    def __init__(self, provider: Provider[T]) -> None:
        ...

    def in_context(self) -> bool:
        """Returns if `.open()` or `.begin()` calls where made inside an open context"""

    @property
    def client(self) -> T:
        """Returns a client instance if context is open"""

    def open(self) -> typing.ContextManager[None]:
        """Opens context"""

    def begin(self) -> typing.ContextManager[T]:
        """Returns client from open context or a independent client if no context is open."""


@typing.runtime_checkable
class AbstractAsyncContext(typing.Protocol[T]):
    provider: AsyncProvider[T]
    inside_ctx: bool

    def __init__(self, provider: AsyncProvider[T]) -> None:
        ...

    def in_context(self) -> bool:
        """Returns if `.open()` or `.begin()` calls where made inside an open context"""

    @property
    def client(self) -> T:
        """Returns a client instance if context is open"""

    def open(self) -> typing.AsyncContextManager[None]:
        """Opens context"""

    def begin(self) -> typing.AsyncContextManager[T]:
        """Returns client from open context or a independent client if no context is open."""


class _HasState(typing.Protocol):
    state: typing.Type
    app: "HasState"


class _HasContext(typing.Protocol):
    context: typing.Type
    app: "HasState"


class _HasCtx(typing.Protocol):
    ctx: typing.Type
    app: "HasState"


HasState = typing.Union[_HasState, _HasContext, _HasCtx]


class StateWrapper:
    _valid_state_attrs = ["state", "context", "app"]

    def __init__(self, has_state: HasState) -> None:
        self.has_state = has_state
        self._validate_instance()
        self._instance_state_attr = self._get_state_attr(self.has_state)
        self._app_state_attr = self._get_state_attr(self.has_state.app)

    def _validate_instance(self):
        if not hasattr(self.has_state, "app"):
            raise TypeError("State Handler must have 'app' attribute")

    def _get_state_attr(self, instance: HasState):
        for item in self._valid_state_attrs:
            if hasattr(instance, item):
                return item
        else:
            raise NotImplementedError(
                "State Handler does not have supported state_attrs"
            )

    @property
    def _app_state(self):
        return getattr(self.has_state.app, self._app_state_attr)

    @property
    def _instance_state(self):
        return getattr(self.has_state, self._app_state_attr)

    @staticmethod
    def _get(state: type, name: str, _cast: type[T]) -> typing.Optional[T]:
        try:
            val = getattr(state, name)
        except AttributeError:
            return None
        else:
            return val

    @staticmethod
    def _set(state: type, name: str, val: typing.Any):
        setattr(state, name, val)

    def app_get(self, name: str, _cast: type[T] = typing.Any) -> typing.Optional[T]:
        return self._get(self._app_state, name, _cast)

    def get(self, name: str, _cast: type[T] = typing.Any) -> typing.Optional[T]:
        return self._get(self._instance_state, name, _cast)

    def app_set(self, name: str, val: typing.Any):
        self._set(self._app_state, name, val)

    def set(self, name: str, val: typing.Any):
        self._set(self._instance_state, name, val)


class AbstractSyncContextFactory(typing.Protocol[T]):
    """Creates a Context Factory to handle contexts inside a state"""

    _provider_class: type[Provider[T]]
    _context_class: type[AbstractSyncContext[T]]
    _state_name: typing.Optional[str]

    def _get_context(self, state_wrapper: StateWrapper) -> AbstractSyncContext[T]:
        """Initializes Context"""

    def generate_state_name(self) -> str:
        """Returns a key name to store context in state"""

    def has_active_context(
        self, has_state: HasState
    ) -> typing.Optional[AbstractSyncContext[T]]:
        """Returns context from `has_state` if context in has_state, else None"""

    def _set_active_context(
        self, context: AbstractSyncContext[T], state_wrapper: StateWrapper
    ):
        """Sets context in state"""

    def __call__(self, has_state: HasState) -> AbstractSyncContext[T]:
        """Returns context from has_state if exists or opens new context, stores in state, and then returns state"""

    def from_provider(self, provider: type[Provider[T]]):
        """Returns context from a given provider"""


class AbstractAsyncContextFactory(typing.Protocol[T]):
    """Creates a Context Factory to handle contexts inside a state"""

    _provider_class: type[AsyncProvider[T]]
    _context_class: type[AbstractAsyncContext[T]]
    _state_name: typing.Optional[str]

    def _get_context(self, state_wrapper: StateWrapper) -> AbstractAsyncContext[T]:
        """Initializes Context"""

    def generate_state_name(self) -> str:
        """Returns a key name to store context in state"""

    def has_active_context(
        self, has_state: HasState
    ) -> typing.Optional[AbstractAsyncContext[T]]:
        """Returns context from `has_state` if context in has_state, else None"""

    def _set_active_context(
        self, context: AbstractAsyncContext[T], state_wrapper: StateWrapper
    ):
        """Sets context in state"""

    def __call__(self, has_state: HasState) -> AbstractAsyncContext[T]:
        """Returns context from has_state if exists or opens new context, stores in state, and then returns state"""

    def from_provider(self, provider: type[AsyncProvider[T]]):
        """Returns context from a given provider"""
