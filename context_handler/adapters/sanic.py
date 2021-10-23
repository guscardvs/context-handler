import sanic as _sanic

import typing


from context_handler import _datastructures
from context_handler.factory import _ContextFactory


def setup_context_cleaner_middleware(app: _sanic.Sanic):
    async def _context_cleaner_middleware(
        request: _sanic.Request,
        response: _sanic.HTTPResponse,
    ):
        app_state_dict = vars(request.app.ctx)
        request_state_dict = vars(request.ctx)
        provider_list = _get_provider_list(app_state_dict)
        contexts_from_provider = _get_contexts_from_providers(
            provider_list, request_state_dict
        )
        contexts_by_type = _get_contexts_by_type(request_state_dict)
        await _close_active_contexts(
            frozenset(contexts_from_provider + contexts_by_type)
        )
        return response

    app.on_response(_context_cleaner_middleware)


def _get_provider_list(
    _app_state_dict: dict[str, typing.Any]
) -> list[typing.Union[_datastructures.Provider, _datastructures.AsyncProvider]]:
    def _gen():
        for value in _app_state_dict:
            if isinstance(
                value, (_datastructures.Provider, _datastructures.AsyncProvider)
            ):
                yield value

    return list(_gen())


def _get_contexts_from_providers(
    provider_list: list[
        typing.Union[_datastructures.Provider, _datastructures.AsyncProvider]
    ],
    request_state_dict: dict[str, typing.Any],
):
    def _gen():
        for provider in provider_list:
            if (
                context := request_state_dict.get(
                    _ContextFactory.generate_state_name(type(provider))
                )
            ) is not None:
                yield context

    return list(_gen())


def _get_contexts_by_type(request_state_dict: dict[str, typing.Any]):
    def _gen():
        for value in request_state_dict.values():
            if isinstance(
                value,
                (
                    _datastructures.AbstractSyncContext,
                    _datastructures.AbstractAsyncContext,
                ),
            ):
                yield value

    return list(_gen())


async def _close_active_contexts(
    contexts: frozenset[
        typing.Union[
            _datastructures.AbstractAsyncContext, _datastructures.AbstractSyncContext
        ]
    ]
):
    for ctx in contexts:
        if ctx.client is not None:
            if ctx.provider.is_closed(ctx.client):
                if isinstance(ctx.provider, _datastructures.AsyncProvider):
                    await ctx.provider.close_client(ctx.client)
                else:
                    ctx.provider.close_client(ctx.client)
