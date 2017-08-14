# Include standard modules
import asyncio
import logging
import json

# Include 3rd-party modules
from aiohttp import web

# Include DPL modules
from adpl.api import ApiGateway

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


def make_error_response(status: int, message: str) -> web.Response:
    """
    Creates a simple response with specified error code and explanatory message
    :param status: status code of the response
    :param message: explanatory message
    :return: created response
    """
    return web.Response(body="{0}: {1}".format(status, message), status=status)


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


class RestApi(object):
    """
    RestApi is a provider of REST API implementation which receives
    REST requests from clients and passes them to ApiGateway
    """
    def __init__(self, gateway: ApiGateway, loop=None):
        """
        Constructor. Receives a reference to API Gateway that will receive and process all
        command and data requests
        :param gateway: an instance of ApiGateway
        """
        self._gateway = gateway

        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

    async def create_rest_server(self) -> None:
        """
        Factory function that creates fully-functional aiohttp server,
        setups its routes and request handlers.
        :param loop: EventLoop to create server in
        :return: None
        """
        dispatcher = web.UrlDispatcher()
        dispatcher.add_get(path='/', handler=self.root_get_handler)
        dispatcher.add_post(path='/auth', handler=self.auth_post_handler)
        dispatcher.add_get(path='/things/', handler=self.things_get_handler)
        dispatcher.add_get(path='/things/{id}', handler=self.thing_get_handler)

        dproxy = DispatcherProxy(dispatcher)

        server = web.Server(handler=dproxy.dispatch)

        # TODO: Make server params configurable
        await self._loop.create_server(server, host='localhost', port='10800')

    async def root_get_handler(self, request: web.Request) -> web.Response:
        """
        A handler for GET requests to path='/'
        :param request: request to be processed
        :return: a response to request
        """
        return make_json_response(
            {"things": "/things/",
             "auth": "/auth"}
        )

    async def auth_post_handler(self, request: web.Request) -> web.Response:
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

        try:
            token = self._gateway.auth(username, password)
            return make_json_response({"message": "authorized", "token": token})

        except ValueError:
            return make_error_response(status=401, message="Access is forbidden. Please, "
                                                           "check your username and password combination")

    async def things_get_handler(self, request: web.Request) -> web.Response:
        """
        A handler for GET requests for path /things/
        :param request: request to be processed
        :return: a response to request
        """
        headers = request.headers  # type: dict

        token = headers.get("Authorization", None)

        if token is None:
            return make_error_response(status=401, message="Authorization header is not available or is null")

        try:
            things = self._gateway.get_things(token)

            return make_json_response({"things": things})
        except PermissionError as e:
            return make_error_response(status=400, message=e.args)

    def _get_thing_id(self, request: web.Request) -> str:
        url = request.rel_url  # type: web.URL
        thing_id = url.path.replace('/things/', '')

        return thing_id

    async def thing_get_handler(self, request: web.Request) -> web.Response:
        """
        A handler for GET requests for path /things/
        :param request: request to be processed
        :return: a response to request
        """
        headers = request.headers  # type: dict

        token = headers.get("Authorization", None)

        if token is None:
            return make_error_response(status=401, message="Authorization header is not available or is null")

        # thing_id = request.match_info['id']
        thing_id = self._get_thing_id(request)

        try:
            thing = self._gateway.get_thing(token, thing_id)

            return make_json_response(thing)
        except PermissionError as e:
            return make_error_response(status=400, message=e.args)

