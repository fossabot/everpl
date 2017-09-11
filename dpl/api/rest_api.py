# Include standard modules
import asyncio
import json
import warnings
import logging
import traceback

# Include 3rd-party modules
from aiohttp import web

# Include DPL modules
from dpl.api import ApiGateway
from dpl.utils import JsonEnumEncoder, filtering
from . import exceptions


# Declare constants:
CONTENT_TYPE_JSON = "application/json"


# Init logger
LOGGER = logging.getLogger(__name__)


def make_error_response(message: str, status: int = 400) -> web.Response:
    """
    Creates a simple JSON response with specified error code and explanatory message
    :param message: explanatory message
    :param status: status code of the response
    :return: created response
    """
    return make_json_response(
        content={"status": status, "message": message},
        status=status
    )


def make_json_response(content: object, status: int = 200) -> web.Response:
    """
    Serialize given content to JSON and create a corresponding response.

    web.json_response() method was not used because it doesn't support usage of
    custom JSON encoders by default (functools.partial() may be used to create a
    corresponding callable which must to be passed into 'json_response' function
    as 'dumps' keyword argument).

    :param content: content to serialize
    :param status: status code of the response
    :return: created response
    """
    serialized = json.dumps(obj=content, cls=JsonEnumEncoder)
    response = web.Response(status=status)
    response.content_type = CONTENT_TYPE_JSON
    response.body = serialized

    return response


def restricted_access_decorator(decorated_callable):
    async def proxy(self, request, *args, **kwargs):
        headers = request.headers  # type: dict

        token = headers.get("Authorization", None)

        if token is None:
            return make_error_response(status=401, message="Authorization header is not available or is null")

        return await decorated_callable(self, request, *args, **kwargs, token=token)

    return proxy


def json_decode_decorator(decorated_callable):
    async def proxy(self, request, *args, **kwargs):
        if request.content_type != CONTENT_TYPE_JSON:
            return make_error_response(status=400, message="Invalid request content-type")

        try:
            json_data = await request.json()  # type: dict
        except json.JSONDecodeError:
            return make_error_response(
                status=400,
                message="Request body content must to be a valid JSON. But it wasn't"
            )

        return await decorated_callable(self, request, *args, **kwargs, json_data=json_data)

    return proxy


class RestApi(object):
    """
    RestApi is a provider of REST API implementation which receives
    REST requests from clients and passes them to ApiGateway.
    """
    def __init__(self, gateway: ApiGateway, loop=None):
        """
        Constructor. Receives a reference to API Gateway that will receive and process all
        command and data requests. Setups API routes and request handlers.

        :param gateway: an instance of ApiGateway
        """
        self._gateway = gateway
        self._handler = None  # callable that returns a Protocol instance
        self._server = None  # type: asyncio.AbstractServer

        self._app = web.Application(
            middlewares=(self._middleware_process_exceptions,)
        )

        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        router = self._app.router  # type: web.UrlDispatcher

        router.add_get(path='/', handler=self.root_get_handler)
        router.add_post(path='/auth', handler=self.auth_post_handler)
        router.add_route(method='OPTIONS', path='/auth', handler=self.auth_options_handler)
        router.add_get(path='/things/', handler=self.things_get_handler)
        router.add_get(path='/things/{id}', handler=self.thing_get_handler)
        router.add_post(path='/messages/', handler=self.messages_post_handler)
        router.add_route(method='OPTIONS', path='/messages/', handler=self.messages_options_handler)
        router.add_get(path='/placements/', handler=self.placements_get_handler)
        router.add_get(path='/placements/{id}', handler=self.placement_get_handler)

    async def create_server(self, host: str, port: int) -> None:
        """
        Factory function that creates fully-functional aiohttp server

        :param host: a server hostname or address
        :param port: a server port
        :return: None
        """
        self._handler = self._app.make_handler(loop=self._loop)
        self._server = await self._loop.create_server(self._handler, host, port)

    async def shutdown_server(self) -> None:
        """
        Stop (shutdown) REST server gracefully.
        More info is available here: http://aiohttp.readthedocs.io/en/stable/web.html#aiohttp-web-graceful-shutdown

        :return: None
        """
        self._server.close()
        await self._server.wait_closed()
        await self._app.shutdown()  # fires on_shutdown signal (so does nothing now)
        await self._handler.shutdown(60.0)
        await self._app.cleanup()  # fires on_cleanup signal (so does nothing now)

    @staticmethod
    async def _middleware_process_exceptions(app, handler):
        """
        Factory method that returns a handler coroutine for all unprocessed exceptions

        :param app: application that is related to this middleware
        :param handler: a handler to be wrapped; original request handler
        :return: a coroutine, middleware handler
        """
        async def middleware_handler(request: web.Request) -> web.Response:
            """
            A function that wraps original request handler called 'handler' and processes
            any unhandled exceptions.
            :param request: request to be handled
            :return: a response to request
            """
            try:
                return await handler(request)

            except web.HTTPMethodNotAllowed:
                return make_error_response(
                    status=405,
                    message="Method {0} is now allowed for this resource".format(request.method)
                )

            except web.HTTPNotFound:
                return make_error_response(
                    status=404,
                    message="Resource {0} was not found".format(request.path)
                )

            except Exception as e:
                LOGGER.error("Unhandled exception in request handling: %s %s\n%s", type(e), e, traceback.format_exc())

                return make_error_response(
                    status=500,
                    message="Server got itself into trouble."
                )

        return middleware_handler

    async def root_get_handler(self, request: web.Request) -> web.Response:
        """
        A handler for GET requests to path='/'

        :param request: request to be processed
        :return: a response to request
        """
        return make_json_response(
            {"things": "/things/",
             "auth": "/auth",
             "messages": "/messages/",
             "placements": "/placements/"}
        )

    @json_decode_decorator
    async def auth_post_handler(self, request: web.Request, json_data: dict = None) -> web.Response:
        """
        Primitive username and password validator

        :param request: request to be processed
        :param json_data: a content of request body
        :return: a response to request
        """
        data = json_data

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

    async def auth_options_handler(self, request: web.Request) -> web.Response:
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

    @staticmethod
    def _params_to_thing_filter_pattern(request: web.Request) -> dict:
        """
        Fetch field names and their values from HTTP request query parameters
        and save them to new dictionary object that can be used for filtering of things.

        :param request: request to be processed
        :return: a dict, filter pattern
        """
        # Specified a set of fields that are allowed for filtering
        # (like here: https://goo.gl/KUBHTZ)
        filter_fields = ('placement', 'type')

        result = dict()
        query_params = request.query

        for field_name in filter_fields:
            if field_name in query_params:
                result[field_name] = query_params[field_name]

        return result

    @restricted_access_decorator
    async def things_get_handler(self, request: web.Request, token: str = None) -> web.Response:
        """
        A handler for GET requests for path /things/

        :param request: request to be processed
        :param token: an access token to be used, usually fetched by restricted_access_decorator
        :return: a response to request
        """
        try:
            things = self._gateway.get_things(token)
            pattern = self._params_to_thing_filter_pattern(request)

            filtered = filtering.filter_items(things, pattern)

            return make_json_response({"things": filtered})
        except PermissionError as e:
            return make_error_response(status=400, message=str(e))

    def _get_thing_id(self, request: web.Request) -> str:
        thing_id = request.match_info['id']

        return thing_id

    @restricted_access_decorator
    async def thing_get_handler(self, request: web.Request, token: str = None) -> web.Response:
        """
        A handler for GET requests for path /things/

        :param request: request to be processed
        :param token: an access token to be used, usually fetched by restricted_access_decorator
        :return: a response to request
        """
        thing_id = self._get_thing_id(request)

        try:
            thing = self._gateway.get_thing(token, thing_id)

            return make_json_response(thing)

        except exceptions.ThingNotFoundError:
            return make_error_response(
                message="Failed to find a thing with the specified ID",
                status=404
            )

        except PermissionError as e:
            return make_error_response(status=400, message=str(e))

    @restricted_access_decorator
    async def placements_get_handler(self, request: web.Request, token: str = None) -> web.Response:
        """
        A handler for GET requests for path /placements/

        :param request: request to be processed
        :param token: an access token to be used, usually fetched by restricted_access_decorator
        :return: a response to request
        """
        try:
            return make_json_response(
                {"placements": self._gateway.get_placements(token)}
            )
        except PermissionError:
            return make_error_response(
                message="This token doesn't permit viewing of placement data",
                status=403
            )

    def _get_placement_id(self, request: web.Request) -> str:
        placement_id = request.match_info['id']

        return placement_id

    @restricted_access_decorator
    async def placement_get_handler(self, request: web.Request, token: str = None) -> web.Response:
        """
        A handler for GET requests for path /placements/

        :param request: request to be processed
        :param token: an access token to be used, usually fetched by restricted_access_decorator
        :return: a response to request
        """
        placement_id = self._get_placement_id(request)

        try:
            return make_json_response(self._gateway.get_placement(token, placement_id))

        except exceptions.PlacementNotFoundError:
            return make_error_response(
                message="Failed to find a placement with the specified ID",
                status=404
            )

        except PermissionError:
            return make_error_response(
                message="This token doesn't permit viewing of placement data",
                status=403
            )

    @restricted_access_decorator
    @json_decode_decorator
    async def messages_post_handler(self, request: web.Request, token: str = None, json_data: dict = None) -> web.Response:
        """
        ONLY FOR COMPATIBILITY: Accept 'action requested' messages from clients.
        Handle POST requests for /messages/ path.

        :param request: request to be processed
        :param token: an access token to be used, usually fetched by restricted_access_decorator
        :return: a response to request
        """
        warnings.warn(PendingDeprecationWarning)

        request_body = json_data

        msg_type = request_body.get("type", None)

        if msg_type is None:
            return make_error_response(status=400, message="Invalid message format: missing 'type' value")

        if msg_type != "user_request":
            return make_error_response(
                status=400,
                message="Unsupported message type: {0}. "
                        "Only type='user_request' is supported".format(msg_type)
            )

        msg_event = request_body.get("event", None)

        if msg_event != "action_requested":
            return make_error_response(
                status=400,
                message="Unsupported event specified: {0}. "
                        "Only event='action_requested' is supported".format(msg_event)
            )

        msg_body = request_body.get("body", None)  # type: dict

        if not isinstance(msg_body, dict):
            return make_error_response(
                status=400,
                message="Message body is invalid or absent."
            )

        # TODO: Consider consolidation of error messages and adding of link to knowledge base

        thing_action = msg_body.get("action", None)  # type: str

        if thing_action is None:
            return make_error_response(
                status=400,
                message="Requested action is not specified in message body or is null."
            )

        thing_id = msg_body.get("obj_id", None)  # type: str

        if thing_id is None:
            return make_error_response(
                status=400,
                message="obj_id (unique identifier of specific Thing)"
                        "is not specified or is null."
            )

        thing_action_params = msg_body.get("action_params", None)  # type: dict

        if not isinstance(thing_action_params, dict):
            return make_error_response(
                status=400,
                message="A value of action_params is invalid or absent."
                        "It must be a dictionary that contains all parameters"
                        "that need to be passed to thing to perform the specified action."
            )

        try:
            self._gateway.send_command(token, thing_id, thing_action, **thing_action_params)
        except PermissionError as e:
            return make_error_response(
                status=403,
                message=str(e)
            )
        except ValueError as e:
            return make_error_response(
                status=400,
                message=str(e)
            )

        return make_json_response(
            content={"message": "accepted"},
            status=202
        )

    async def messages_options_handler(self, request: web.Request) -> web.Response:
        """
        A handler for OPTIONS request for path /messages/.

        Returns a response that contains 'Allow' header with all allowed HTTP methods.

        :param request: request to be handled
        :return: a response to request
        """
        return web.Response(
            body=None,
            status=204,
            headers={'Allow': 'POST, HEAD, OPTIONS'}
        )

