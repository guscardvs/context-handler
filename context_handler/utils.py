import typing
from functools import wraps
from inspect import isasyncgenfunction, iscoroutinefunction

from typing_extensions import Concatenate, ParamSpec

from . import _datastructures

T = typing.TypeVar("T")
P = ParamSpec("P")
ClassT = typing.TypeVar("ClassT")


class _EnsureContext:
    def function(
        self,
        func: typing.Callable[Concatenate[_datastructures.AbstractSyncContext, P], T],
    ) -> typing.Callable[Concatenate[_datastructures.AbstractSyncContext, P], T]:
        if iscoroutinefunction(func):

            @wraps(func)
            async def inner(
                context: _datastructures.AbstractSyncContext,
                *args: P.args,
                **kwargs: P.kwargs,
            ):
                with context.open():
                    error = None
                    try:
                        result = await func(context, *args, **kwargs)  # type: ignore
                    except Exception as err:
                        error = err
                    else:
                        return result
                raise error

        elif isasyncgenfunction(func):

            @wraps(func)
            async def inner(
                context: _datastructures.AbstractSyncContext,
                *args: P.args,
                **kwargs: P.kwargs,
            ):
                with context.open():
                    error = None
                    try:
                        async for item in func(context, *args, **kwargs):  # type: ignore
                            yield item
                    except Exception as err:
                        error = err
                if error is not None:
                    raise error

        else:

            @wraps(func)
            def inner(
                context: _datastructures.AbstractSyncContext,
                *args: P.args,
                **kwargs: P.kwargs,
            ):
                with context.open():
                    error = None
                    try:
                        result = func(context, *args, **kwargs)  # type: ignore
                    except Exception as err:
                        error = err
                    else:
                        return result
                raise error

        return inner

    def _method(self, context_attr_name: str):
        def outer(
            func: typing.Callable[Concatenate[ClassT, P], T],
        ) -> typing.Callable[Concatenate[ClassT, P], T]:
            def context_getter(instance: ClassT) -> _datastructures.AbstractSyncContext:
                return getattr(instance, context_attr_name)

            if iscoroutinefunction(func):

                @wraps(func)
                async def inner(instance: ClassT, *args: P.args, **kwargs: P.kwargs):
                    with context_getter(instance).open():
                        error = None
                        try:
                            result = await func(instance, *args, **kwargs)  # type: ignore
                        except Exception as err:
                            error = err
                        else:
                            return result
                    raise error

            elif isasyncgenfunction(func):

                @wraps(func)
                async def inner(instance: ClassT, *args: P.args, **kwargs: P.kwargs):
                    with context_getter(instance).open():
                        error = None
                        try:
                            async for item in func(instance, *args, **kwargs):  # type: ignore
                                yield item
                        except Exception as err:
                            error = err
                    if error is not None:
                        raise error

            else:

                @wraps(func)
                def inner(instance: ClassT, *args: P.args, **kwargs: P.kwargs):
                    with context_getter(instance).open():
                        error = None
                        try:
                            result = func(instance, *args, **kwargs)  # type: ignore
                        except Exception as err:
                            error = err
                        else:
                            return result
                    raise error

            return inner

    def method(
        self,
        func: typing.Callable[Concatenate[ClassT, P], T] = None,
        /,
        *,
        context_attr_name: str = "context",
    ) -> typing.Callable[
        [typing.Callable[Concatenate[ClassT, P], T]],
        typing.Callable[Concatenate[ClassT, P], T],
    ]:
        wrapper = self._method(context_attr_name)
        if func:
            return wrapper(func)  # type: ignore
        return wrapper  # type: ignore

    def awaitable(
        self,
        func: typing.Callable[Concatenate[_datastructures.AbstractAsyncContext, P], T],
    ) -> typing.Callable[Concatenate[_datastructures.AbstractAsyncContext, P], T]:
        if iscoroutinefunction(func):

            @wraps(func)
            async def inner(
                context: _datastructures.AbstractAsyncContext,
                *args: P.args,
                **kwargs: P.kwargs,
            ):
                async with context.open():
                    error = None
                    try:
                        result = await func(context, *args, **kwargs)  # type: ignore
                    except Exception as err:
                        error = err
                    else:
                        return result
                raise error

        elif isasyncgenfunction(func):

            @wraps(func)
            async def inner(
                context: _datastructures.AbstractAsyncContext,
                *args: P.args,
                **kwargs: P.kwargs,
            ):
                async with context.open():
                    error = None
                    try:
                        async for item in func(context, *args, **kwargs):  # type: ignore
                            yield item
                    except Exception as err:
                        error = err
                if error is not None:
                    raise error

        else:
            raise NotImplementedError
        return inner

    def _async_method(self, context_attr_name: str):
        def outer(
            func: typing.Callable[Concatenate[ClassT, P], T],
        ) -> typing.Callable[Concatenate[ClassT, P], T]:
            def context_getter(
                instance: ClassT,
            ) -> _datastructures.AbstractAsyncContext:
                return getattr(instance, context_attr_name)

            if iscoroutinefunction(func):

                @wraps(func)
                async def inner(instance: ClassT, *args: P.args, **kwargs: P.kwargs):
                    async with context_getter(instance).open():
                        error = None
                        try:
                            result = await func(instance, *args, **kwargs)  # type: ignore
                        except Exception as err:
                            error = err
                        else:
                            return result
                    raise error

            elif isasyncgenfunction(func):

                @wraps(func)
                async def inner(instance: ClassT, *args: P.args, **kwargs: P.kwargs):
                    async with context_getter(instance).open():
                        error = None
                        try:
                            async for item in func(instance, *args, **kwargs):  # type: ignore
                                yield item
                        except Exception as err:
                            error = err
                    if error is not None:
                        raise error

            else:
                raise NotImplementedError

            return inner

    def async_method(
        self,
        func: typing.Callable[Concatenate[ClassT, P], T] = None,
        /,
        *,
        context_attr_name: str = "context",
    ) -> typing.Callable[
        [typing.Callable[Concatenate[ClassT, P], T]],
        typing.Callable[Concatenate[ClassT, P], T],
    ]:
        wrapper = self._async_method(context_attr_name)
        if func:
            return wrapper(func)  # type: ignore
        return wrapper  # type: ignore


ensure_context = _EnsureContext()
