# Include standard modules
import asyncio
import logging
import json

# Include 3rd-party modules
from aiohttp import web

# Include DPL modules
from adpl.auth import User

# Declare constants:
CONTENT_TYPE_JSON = "application/json"


class DispatcherProxy(object):
    """
    Support class that allows web.AbstractRouter usage with plain web.Server objects.

    Has one coroutine 'dispatch' that receives request, resolve corresponding
    handler from web.AbstractRouter and calls found handler.
    """
    def __init__(self, router: web.AbstractRouter):
        """
        Constructor
        :param router: an instance for web.AbstractRouter that need to be wrapped.
        """
        self._router = router

    async def dispatch(self, request: web.Request) -> web.Response:
        """
        Dispatch: pre-handle request and pass it to corresponding handler
        :param request: request to be processed
        :return: a response to request
        """
        resolved = await self._router.resolve(request)  # type: web.AbstractMatchInfo
        return await resolved.handler(request)


def make_json_response(content: object) -> web.Response:
    """
    Serialize given content to JSON and create corresponding response
    :param content: content to serialize
    :return: created response
    """
    serialized = json.dumps(obj=content)
    response = web.Response()
    response.content_type = CONTENT_TYPE_JSON
    response.body = serialized

    return response


def make_error_response(status: int, message: str) -> web.Response:
    """
    Creates a simple response with specified error code and explanatory message
    :param status: status code of the response
    :param message: explanatory message
    :return: created response
    """
    return web.Response(body="{0}: {1}".format(status, message), status=status)


async def create_rest_server(loop: asyncio.AbstractEventLoop) -> None:
    """
    Factory function that creates fully-functional aiohttp server,
    setups its routes and request handlers.
    :param loop: EventLoop to create server in
    :return: None
    """
    dispatcher = web.UrlDispatcher()
    dispatcher.add_get(path='/', handler=root_get_handler)
    dispatcher.add_get(path='/json_sample', handler=json_get_handler)
    dispatcher.add_post(path='/auth', handler=auth_post_handler)

    dproxy = DispatcherProxy(dispatcher)

    server = web.Server(handler=dproxy.dispatch)
    await loop.create_server(server, host='localhost', port='8888')


async def root_get_handler(request: web.Request) -> web.Response:
    """
    Primitive handler for requests with path='/' and method='GET'
    :param request: request to be handled
    :return: a response to request
    """
    response_text = "Hello, world!"
    return web.Response(text=response_text, status=200)


async def json_get_handler(request: web.Request) -> web.Response:
    """
    Primitive handler for requests with path='/json_sample' and method='GET'
    :param request: request to be handled
    :return: a response to request
    """
    return make_json_response(
        {"text": "Hello, world!", "status": 200}
    )


SAMPLE_USER = User(username="Foo", password="Bar")


async def auth_post_handler(request: web.Request) -> web.Response:
    """
    Primitive username and password validator
    :param request: request to be processed
    :return: a response to request
    """
    if request.content_type != CONTENT_TYPE_JSON:
        return web.Response(body="400: Invalid request content-type", status=400)

    data = await request.json()  # type: dict

    username = data.get("username", None)
    password = data.get("password", None)

    if username is None:
        return make_error_response(status=400, message="Username is not specified or is null")

    if password is None:
        return make_error_response(status=400, message="Password is not specified or is null")

    if username == SAMPLE_USER.username and SAMPLE_USER.verify_password(password):
        return make_json_response({"token": "12345678"})

    else:
        # Fixme: CC1: Change status to 401?
        return make_error_response(status=403, message="Access is forbidden. Please, "
                                                       "check your username and password combination")
