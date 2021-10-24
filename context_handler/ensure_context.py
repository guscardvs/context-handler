import typing
from functools import partial, wraps
from inspect import isasyncgenfunction, iscoroutinefunction
from types import SimpleNamespace

from typing_extensions import ParamSpec

from . import _datastructures, context

T = typing.TypeVar("T")
P = ParamSpec("P")
ClassT = typing.TypeVar("ClassT")


def _open_sync_ctx_in_sync(
    getter: _datastructures.ContextGetter,
    func,
    first_arg,
    *args,
    **kwargs,
):
    with getter.get(first_arg).open():
        return func(first_arg, *args, **kwargs)  # type: ignore


async def _open_sync_ctx_in_coro(
    getter: _datastructures.ContextGetter,
    func,
    first_arg,
    *args,
    **kwargs,
):
    with getter.get(first_arg).open():
        return await func(first_arg, *args, **kwargs)  # type: ignore


async def _open_sync_ctx_in_asyncgen(
    getter: _datastructures.ContextGetter,
    func,
    first_arg,
    *args,
    **kwargs,
):
    with getter.get(first_arg).open():
        async for item in func(first_arg, *args, **kwargs):  # type: ignore
            yield item


async def _open_async_ctx_in_coro(
    getter: _datastructures.ContextGetter,
    func,
    first_arg,
    *args,
    **kwargs,
):
    async with getter.get(first_arg).open():
        return await func(first_arg, *args, **kwargs)  # type: ignore


async def _open_async_ctx_in_async_gen(
    getter: _datastructures.ContextGetter,
    func,
    first_arg,
    *args,
    **kwargs,
):
    async with getter.get(first_arg).open():
        async for item in func(first_arg, *args, **kwargs):  # type: ignore
            yield item


def _setup_wrapper(wrapper: typing.Callable, func, context_getter):
    @wraps(func)
    def wrapped(*args, **kwargs):
        return wrapper(context_getter, func, *args, **kwargs)

    return wrapped


def _get_sync_wrapper(func):
    inner = _open_sync_ctx_in_sync
    if isasyncgenfunction(func):
        inner = _open_sync_ctx_in_asyncgen
    elif iscoroutinefunction(func):
        inner = _open_sync_ctx_in_coro
    return inner


def _get_async_wrapper(func):
    if iscoroutinefunction(func):
        inner = _open_async_ctx_in_coro
    elif isasyncgenfunction(func):
        inner = _open_async_ctx_in_async_gen
    else:
        raise TypeError("AsyncContext cannot be used in sync function")
    return inner


@typing.overload
def sync_context(
    *,
    first_arg_type: typing.Literal["instance"],
    context_attr_name: str,
) -> typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]]:
    ...


@typing.overload
def sync_context(
    *,
    first_arg_type: typing.Literal["view"],
    _factory: typing.Union[
        _datastructures.AbstractAsyncContextFactory,
        _datastructures.AbstractSyncContextFactory,
    ],
) -> typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]]:
    ...


@typing.overload
def sync_context(
    *,
    first_arg_type: typing.Literal["context"],
) -> typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]]:
    ...


@typing.overload
def sync_context(
    func: typing.Callable[P, T],
    /,
) -> typing.Callable[P, T]:
    ...


def sync_context(
    func: typing.Callable[P, T] = None,
    /,
    *,
    first_arg_type: typing.Union[
        typing.Literal["instance"],
        typing.Literal["view"],
        typing.Literal["context"],
    ] = "context",
    **kwargs,
) -> typing.Union[
    typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]],
    typing.Callable[P, T],
]:
    context_getter = _datastructures.ContextGetter(
        _datastructures.ContextGetter.ArgType.get(first_arg_type),
        **kwargs,
    )

    def outer(func):
        return _setup_wrapper(_get_sync_wrapper(func), func, context_getter)

    if func:
        return outer(func)
    return outer


@typing.overload
def async_context(
    *,
    first_arg_type: typing.Literal["instance"],
    context_attr_name: str,
) -> typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]]:
    ...


@typing.overload
def async_context(
    *,
    first_arg_type: typing.Literal["view"],
    _factory: typing.Union[
        _datastructures.AbstractAsyncContextFactory,
        _datastructures.AbstractSyncContextFactory,
    ],
) -> typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]]:
    ...


@typing.overload
def async_context(
    *,
    first_arg_type: typing.Literal["context"],
) -> typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]]:
    ...


@typing.overload
def async_context(
    func: typing.Callable[P, T],
    /,
) -> typing.Callable[P, T]:
    ...


def async_context(
    func: typing.Callable[P, T] = None,
    /,
    *,
    first_arg_type: typing.Union[
        typing.Literal["instance"],
        typing.Literal["view"],
        typing.Literal["context"],
    ] = "context",
    **kwargs,
) -> typing.Union[
    typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]],
    typing.Callable[P, T],
]:
    context_getter = _datastructures.ContextGetter(
        _datastructures.ContextGetter.ArgType.get(first_arg_type),
        **kwargs,
    )

    def outer(func):
        return _setup_wrapper(_get_async_wrapper(func), func, context_getter)

    if func:
        return outer(func)  # type: ignore
    return outer


def _guess_context_class(
    provider_class: type[
        typing.Union[_datastructures.Provider, _datastructures.AsyncProvider]
    ]
):
    if issubclass(provider_class, _datastructures.AsyncProvider):
        return context.AsyncContext
    elif issubclass(provider_class, _datastructures.Provider):
        return context.SyncContext
    raise TypeError(
        "provider_class must implement either _datastructures.Provider or _datastructures.AsyncProvider protocol"
    )


__all__ = ["sync_context", "async_context"]
