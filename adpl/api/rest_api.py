# Include standard modules
import asyncio
import logging

# Include 3rd-party modules
from aiohttp import web

# Include DPL modules


class DispatcherProxy(object):
    def __init__(self, router: web.AbstractRouter):
        self._router = router

    async def dispatch(self, request: web.Request):
        resolved = await self._router.resolve(request)  # type: web.AbstractMatchInfo
        return await resolved.handler(request)


async def create_rest_server(loop):
    dispatcher = web.UrlDispatcher()
    dispatcher.add_get(path='/', handler=root_get_handler)

    dproxy = DispatcherProxy(dispatcher)

    server = web.Server(handler=dproxy.dispatch)
    await loop.create_server(server, host='localhost', port='8888')


async def root_get_handler(request: web.Request):
    response_text = "Hello, world!"
    return web.Response(text=response_text, status=200)
