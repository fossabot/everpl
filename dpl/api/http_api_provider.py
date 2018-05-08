"""
This module contains a base HTTP API Provider implementation. This provider
is only used to merge different HTTP-based API providers under the same domain
"""
import asyncio

from aiohttp import web


class HttpApiProvider(object):
    """
    This class contains a base HTTP provider to be used
    """

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        self._handler = None
        self._server = None

        self._app = web.Application()

    def add_child_provider(self, provider, provider_root: str) -> None:
        """
        Assigns the specified address to the specified API provider

        :param provider: an child API provider to be registered
        :param provider_root: an address where this provider will be installed
        :return: None
        """
        self._app.add_subapp(
            provider_root, provider.app
        )

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
        Stop (shutdown) REST server gracefully.
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
