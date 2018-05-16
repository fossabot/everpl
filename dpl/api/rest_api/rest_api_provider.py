import time
import logging
import traceback
import asyncio

import aiohttp.web as web

from dpl.auth.auth_context import AuthContext
from dpl.auth.abs_auth_service import (
    AbsAuthService,
    AuthInvalidUserPasswordCombinationError
)
from dpl.api.cors_middleware import CorsMiddleware
from dpl.api.api_errors import ERROR_TEMPLATES
from dpl.api.http_api_provider import HttpApiProvider

from .common import make_json_response
from .json_decode_decorator import json_decode_decorator

# Init logger
LOGGER = logging.getLogger(__name__)


@web.middleware
async def middleware_process_exceptions(request: web.Request,
                                        handler) -> web.Response:
    """
    A function that wraps original request handler called
    'handler' and processes any unhandled exceptions.

    :param request: request to be handled
    :return: a response to request
    """
    try:
        return await handler(request)

    except web.HTTPMethodNotAllowed:
        error_dict = ERROR_TEMPLATES[1004].to_dict()
        error_dict["devel_message"] = error_dict["devel_message"].format(
            method_name=request.method)

        return make_json_response(
            status=405,
            content=error_dict
        )

    except web.HTTPNotFound:
        return make_json_response(
            status=404,
            content=ERROR_TEMPLATES[1005].to_dict()
        )

    except Exception as e:
        timestamp = time.monotonic()

        LOGGER.error(
            "Unhandled exception in request handling at %s: %s %s\n%s",
            timestamp, type(e), e, traceback.format_exc())

        error_dict = ERROR_TEMPLATES[1003].to_dict()
        error_dict["user_message"] = error_dict["user_message"].format(
            timestamp=timestamp)

        return make_json_response(
            status=500,
            content=error_dict
        )


class RestApiProvider(HttpApiProvider):
    """
    This class contains a logic of a REST API provider.

    It declares some root-level logic and request handlers, sets
    routes for subapps and assembles everything together

    ..WARNING: May be removed in the future
    """

    def __init__(
            self, things: web.Application, placements: web.Application,
            auth_context: AuthContext,
            auth_service: AbsAuthService,
            loop: asyncio.AbstractEventLoop = None
    ):
        self._cors_middleware = CorsMiddleware(
            is_enabled=True,
            allowed_origin='*'
        )

        middlewares = (
            self._cors_middleware.handle, middleware_process_exceptions
        )

        super().__init__(loop=loop, middlewares=middlewares)

        self._things = things
        self._placements = placements
        self._auth_context = auth_context
        self._auth_service = auth_service

        self._handler = None
        self._server = None

        context_data = {
            'auth_service': auth_service,
            'auth_context': auth_context
        }

        self._app.update(context_data)

        self._app.add_subapp(
            '/things/', self._things
        )
        self._app.add_subapp(
            '/placements/', self._placements
        )

        self._router = self._app.router  # type: web.UrlDispatcher

        self._router.add_get(path='/', handler=root_get_handler)
        self._router.add_post(path='/auth', handler=auth_post_handler)
        self._router.add_route(
            method='OPTIONS', path='/auth', handler=auth_options_handler
        )


async def root_get_handler(request: web.Request) -> web.Response:
    """
    A handler for GET requests to path='/'

    :param request: request to be processed
    :return: a response to request
    """
    return make_json_response(
        {"things": "/things/",
         "auth": "/auth",
         "placements": "/placements/"}
    )


@json_decode_decorator
async def auth_post_handler(request: web.Request) -> web.Response:
    """
    Primitive username and password validator

    :param request: request to be processed
    :return: a response to request
    """
    data = await request.json()

    username = data.get("username", None)
    password = data.get("password", None)

    if username is None:
        return make_json_response(
            status=400,
            content=ERROR_TEMPLATES[2000].to_dict()
        )

    if password is None:
        return make_json_response(
            status=400,
            content=ERROR_TEMPLATES[2001].to_dict()
        )

    auth_service = request.app['auth_service']

    try:
        token = auth_service.request_access(
            username, password,
            client_info=request.headers.get('User-Agent'),
            client_ip=request.transport.get_extra_info('peername')
        )

        return make_json_response({"message": "authorized", "token": token})

    except AuthInvalidUserPasswordCombinationError:
        return make_json_response(
            status=401,
            content=ERROR_TEMPLATES[2002].to_dict()
        )


async def auth_options_handler(request: web.Request) -> web.Response:
    """
    A handler for OPTIONS request for path /auth.

    Returns a response that contains 'Allow' header with all allowed HTTP methods.

    :param request: request to be handled
    :return: a response to request
    """
    return web.Response(
        body=None,
        status=204,
        headers={'Allow': 'POST, HEAD, OPTIONS'}
    )
