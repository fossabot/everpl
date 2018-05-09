"""
This module contains a definition of Streaming API provider
"""
import asyncio
import json
import time
import random
from typing import Mapping, MutableMapping

from aiohttp import web

from dpl.auth.auth_context import AuthContext
from dpl.auth.abs_auth_service import (
    AbsAuthService,
    AuthInvalidTokenError
)
from dpl.services.service_exceptions import ServiceEntityResolutionError
from dpl.api.api_errors import ERROR_TEMPLATES


class StreamAuthError(Exception):
    pass


def prepare_message(type_: str, topic: str, body: Mapping) -> Mapping:
    """
    Prepares a message to be sent to the client

    :param type_: a type of the message
    :param topic: a topic of the message
    :param body: a body of the message
    :return: a constructed message
    """
    return {
        "timestamp": time.time(),
        "type": type_,
        "topic": topic,
        "body": body
    }


def prepare_error_message(body: Mapping) -> Mapping:
    """
    Constructs an error message to be sent to the client

    :param body: a body of the message
    :return: a constructed message
    """
    return prepare_message(
        type_="control",
        topic="error",
        body=body
    )


async def start_auth_flow(ws: web.WebSocketResponse) -> str:
    """
    Handles the first steps of the client authentication and returns the
    access token specified (send) by client

    :param ws: an instance of WebSocketResponse for receiving of and sending
           messages
    :return: an access token specified by client
    """
    try:
        received = await ws.receive_json(timeout=20)  # type: dict
    except TypeError as e:
        exception_arg = e.args[0]  # type: str
        got_type = exception_arg[17:exception_arg.index(":")]

        error = ERROR_TEMPLATES[5000].to_dict()
        error['devel_message'] = error['devel_message'] % ('TEXT', got_type)
        message = prepare_error_message(error)
        ws.send_json(data=message)
        raise StreamAuthError()

    except json.JSONDecodeError:
        error = ERROR_TEMPLATES[5001].to_dict()
        message = prepare_error_message(error)
        ws.send_json(message)
        raise StreamAuthError()

    except (asyncio.CancelledError, asyncio.TimeoutError):
        error = ERROR_TEMPLATES[5002].to_dict()
        error['devel_message'] = error['devel_message'] % '20 seconds'
        message = prepare_error_message(error)
        ws.send_json(message)
        raise StreamAuthError()

    msg_type = received.get('type', 'null')

    if msg_type != 'control':
        error = ERROR_TEMPLATES[5003].to_dict()
        error['devel_message'] = error['devel_message'] % msg_type
        message = prepare_error_message(error)
        ws.send_json(message)
        raise StreamAuthError()

    msg_topic = received.get('topic', 'null')

    if msg_topic != 'auth':
        error = ERROR_TEMPLATES[5010].to_dict()
        error['devel_message'] = error['devel_message'] % ('auth', msg_topic)
        message = prepare_error_message(error)
        ws.send_json(message)
        raise StreamAuthError()

    body = received.get('body')

    if not isinstance(body, Mapping):
        error = ERROR_TEMPLATES[5020].to_dict()
        message = prepare_error_message(error)
        ws.send_json(message)
        raise StreamAuthError()

    token = body.get('access_token')

    if not isinstance(token, str):
        error = ERROR_TEMPLATES[5021].to_dict()
        error['devel_message'] = error['devel_message'] % 'access_token'
        message = prepare_error_message(error)
        ws.send_json(message)
        raise StreamAuthError()

    return token


async def handle_incoming_message(
    app: web.Application, ws: web.WebSocketResponse,
    message: dict
) -> None:
    """
    Handles incoming message. Analyzes it, sends a response if needed and
    executes related server-side tasks (like registration of subscriptions)

    :param app: an instance of aiohttp Application which handles all
           environment variables
    :param ws: an instance of WebSocketResponse for receiving of and sending
           messages
    :param message: a message to be handled
    :return: None
    """
    print("RESULT>>>>>>>>>>", message)


async def handle_outcoming_message(
    app: web.Application, ws: web.WebSocketResponse,
    message: dict
) -> None:
    """
    Handles outcoming message i.e. message to be sent to client. Analyzes it
    and sends to the client if appropriate. May schedule a re-send if sending
    was failed.

    :param app: an instance of aiohttp Application which handles all
           environment variables
    :param ws: an instance of WebSocketResponse for receiving of and sending
           messages
    :param message: a message to be handled
    :return: None
    """
    await ws.send_json(message)


async def message_loop(
        app: web.Application, ws: web.WebSocketResponse, session_id: str
) -> None:
    """
    Contains the main loop which handles al the incoming and outcoming Messages

    :param app: an instance of aiohttp Application which handles all
           environment variables
    :param ws: an instance of WebSocketResponse for receiving of and sending
           messages
    :param session_id: an identifier of this Session
    :return: None
    """
    undelivered = app['undelivered']  # type: dict

    queue = undelivered.setdefault(
        session_id, asyncio.Queue()
    )

    print(queue)
    print(queue.qsize())

    queue_cor = queue.get()
    receive_cor = ws.receive()

    queue_cor_task = asyncio.ensure_future(queue_cor)
    receive_cor_task = asyncio.ensure_future(receive_cor)

    while not ws.closed:
        done, pending = await asyncio.wait(
            (queue_cor_task, receive_cor_task),
            return_when=asyncio.FIRST_COMPLETED
        )

        print("gone from wait")
        print(done)
        print(pending)

        if queue_cor_task in done:
            await handle_outcoming_message(
                app=app, ws=ws, message=queue_cor_task.result()
            )
            queue_cor = queue.get()
            queue_cor_task = asyncio.ensure_future(queue_cor)

        if receive_cor_task in done:
            await handle_incoming_message(
                app=app, ws=ws, message=receive_cor_task.result()
            )

            receive_cor = ws.receive_json()
            receive_cor_task = asyncio.ensure_future(receive_cor)


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
        token = await start_auth_flow(ws)

    except StreamAuthError:
        ws.close()
        return ws

    auth_context = request.app['auth_context']  # type: AuthContext
    auth_service = request.app['auth_service']  # type: AbsAuthService
    assert isinstance(auth_context, AuthContext)
    assert isinstance(auth_service, AbsAuthService)

    try:
        session = auth_service.view_current_session(token)
    except ServiceEntityResolutionError:
        error = ERROR_TEMPLATES[2101].to_dict()
        message = prepare_error_message(error)
        ws.send_json(message)
        ws.close()
        return ws

    # everything is fine starting from here
    auth_ack = prepare_message(
        type_="control",
        topic="auth_ack",
        body={}
    )
    ws.send_json(auth_ack)

    try:
        with auth_context(token=token):
            await message_loop(request.app, ws, session['domain_id'])

    except AuthInvalidTokenError:
        error = ERROR_TEMPLATES[2101].to_dict()
        message = prepare_error_message(error)
        ws.send_json(message)
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

        self._undelivered = dict()  # type: MutableMapping[str, asyncio.Queue]

        self._app = web.Application()

        context_data = {
            'auth_service': auth_service,
            'auth_context': auth_context,
            'undelivered': self._undelivered
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

    async def start_sample_loop(self) -> None:
        counter = 0

        while True:
            await asyncio.sleep(random.randint(0, 10))
            for queue in self._undelivered.values():
                await queue.put(
                    prepare_message(
                        type_="data",
                        topic="notification",
                        body={
                            "title": "Example notification",
                            "text": "Hi! #%d" % counter
                        }
                    )
                )
                print(queue)
                print(queue.qsize())

            counter += 1

