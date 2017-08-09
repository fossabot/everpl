# Include standard modules
import asyncio
import logging
import collections

# Include 3rd-party modules
from aiohttp import web

# Include DPL modules

HandlerKey = collections.namedtuple("HandlerKey", ('path', 'method'))


class RequestDispatcher(object):
    def __init__(self):
        self._handlers = dict()  # type: dict[HandlerKey, asyncio.coroutine]

    def add(self, path: str, method: str, handler: asyncio.coroutine):
        """
        Add request handler
        :param path: request path
        :param method: request method
        :param handler: coroutine, request handler itself
        :return: None
        """
        self._handlers[HandlerKey(path, method)] = handler

    async def dispatch(self, request: web.Request) -> web.Response:
        """
        Pass a request to corresponding handler
        :param request: request to handle
        :return: a response to request, passed from handler
        """
        key = HandlerKey(path=request.path, method=request.method)

        handler = self._handlers.get(key, self._handler_404)

        print("Handler got: {0}".format(handler))

        return await handler(request)

    @staticmethod
    async def _handler_404(request: web.Request) -> web.Response:
        """
        Default handler for unknown paths or methods
        :param request: request to handle
        :return: a response to request
        """
        response_text = "404: Not found"
        return web.Response(text=response_text, status=404)


async def create_rest_server(loop):
    dispatcher = RequestDispatcher()

    dispatcher.add(path='/', method='GET', handler=root_get_handler)

    server = web.Server(handler=dispatcher.dispatch)
    await loop.create_server(server, host='localhost', port='8888')


async def root_get_handler(request: web.Request):
    response_text = "Hello, world!"
    return web.Response(text=response_text, status=200)
