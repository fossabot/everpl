"""
This module contains a definition of Streaming API provider
"""
import asyncio

from aiohttp import web

from dpl.api.cors_middleware import CorsMiddleware
from dpl.auth.auth_context import AuthContext
from dpl.auth.abs_auth_service import (
    AbsAuthService,
    AuthInvalidTokenError
)


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

        self._cors_middleware = CorsMiddleware(
            is_enabled=True,
            allowed_origin='*'
        )

        self._app = web.Application(
            middlewares=(self._cors_middleware, )
        )

        context_data = {
            'auth_service': auth_service,
            'auth_context': auth_context
        }

        self._app.update(context_data)

        self._router = self._app.router  # type: web.UrlDispatcher

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
