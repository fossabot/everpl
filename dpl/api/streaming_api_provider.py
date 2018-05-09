"""
This module contains a definition of Streaming API provider
"""
import asyncio
import json
from typing import Mapping

from aiohttp import web

from dpl.auth.auth_context import AuthContext
from dpl.auth.abs_auth_service import (
    AbsAuthService,
    AuthInvalidTokenError
)
from dpl.api.api_errors import ERROR_TEMPLATES


class StreamAuthError(Exception):
    pass


async def handle_auth(ws: web.WebSocketResponse) -> str:
    try:
        received = await ws.receive_json(timeout=20)  # type: dict
    except TypeError as e:
        exception_arg = e.args[0]  # type: str
        got_type = exception_arg[17:exception_arg.index(":")]

        error = ERROR_TEMPLATES[5000].to_dict()
        error['devel_message'] = error['devel_message'] % ('TEXT', got_type)
        ws.send_json(data=error)
        raise StreamAuthError()

    except json.JSONDecodeError:
        error = ERROR_TEMPLATES[5001].to_dict()
        ws.send_json(error)
        raise StreamAuthError()

    except (asyncio.CancelledError, asyncio.TimeoutError):
        error = ERROR_TEMPLATES[5002].to_dict()
        error['devel_message'] = error['devel_message'] % '20 seconds'
        ws.send_json(error)
        raise StreamAuthError()

    msg_type = received.get('type', 'null')

    if msg_type != 'control':
        error = ERROR_TEMPLATES[5003].to_dict()
        error['devel_message'] = error['devel_message'] % msg_type
        ws.send_json(error)
        raise StreamAuthError()

    msg_topic = received.get('topic', 'null')

    if msg_topic != 'auth':
        error = ERROR_TEMPLATES[5010].to_dict()
        error['devel_message'] = error['devel_message'] % ('auth', msg_topic)
        ws.send_json(error)
        raise StreamAuthError()

    body = received.get('body')

    if not isinstance(body, Mapping):
        error = ERROR_TEMPLATES[5020].to_dict()
        ws.send_json(error)
        raise StreamAuthError()

    token = body.get('access_token')

    if not isinstance(token, str):
        error = ERROR_TEMPLATES[5021].to_dict()
        error['devel_message'] = error['devel_message'] % 'access_token'
        ws.send_json(error)
        raise StreamAuthError()

    return token


async def handle_ws_request(request: web.Request) -> web.WebSocketResponse:
    """
    Performs handling of a WS connection handshake, authentication and further
    handling of Streaming API protocol

    :param request: a request to be processed
    :return: an response to request
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    try:
        token = await handle_auth(ws)

    except StreamAuthError:
        ws.close()
        return ws

    try:
        auth_context = request.app['auth_context']  # type: AuthContext
        assert isinstance(auth_context, AuthContext)

        with auth_context(token=token):
            # everything is fine starting from here
            ws.send_str("You did it!")

    except AuthInvalidTokenError:
        ws.send_str("Auth failed: Invalid auth token")
        ws.close()

    return ws


class StreamingApiProvider(object):
    """
    A class that provides a Streaming API of the system. Controls WebSocket
    connections, WS authentication and message sending
    """
    def __init__(
            self, auth_context: AuthContext, auth_service: AbsAuthService,
            loop: asyncio.AbstractEventLoop = None
    ):
        self._auth_context = auth_context
        self._auth_service = auth_service

        self._loop = loop

        self._handler = None
        self._server = None

        self._app = web.Application()

        context_data = {
            'auth_service': auth_service,
            'auth_context': auth_context
        }

        self._app.update(context_data)

        self._router = self._app.router  # type: web.UrlDispatcher
        self._router.add_get(
            path='/',
            handler=handle_ws_request
        )

    @property
    def app(self) -> web.Application:
        """
        Returns the underlying aiohttp.web Application

        :return: the underlying aiohttp.web Application
        """
        return self._app

    async def create_server(self, host: str, port: int) -> None:
        """
        Factory function that creates fully-functional aiohttp server

        :param host: a server hostname or address
        :param port: a server port
        :return: None
        """
        self._handler = self._app.make_handler(loop=self._loop)
        self._server = await self._loop.create_server(
            self._handler, host, port
        )

    async def shutdown_server(self) -> None:
        """
        Stop (shutdown) WS server gracefully.
        More info is available here: https://goo.gl/eNviyZ
        :return: None
        """
        self._server.close()
        await self._server.wait_closed()
        # fires on_shutdown signal (so does nothing now)
        await self._app.shutdown()
        await self._handler.shutdown(60.0)
        # fires on_cleanup signal (so does nothing now)
        await self._app.cleanup()
