"""
This module contains definition of StreamingApiProvider
"""
import asyncio
import logging
import weakref
import functools
from typing import Mapping, Dict, Tuple

from aiohttp import WSCloseCode
from aiohttp.web import Request, WebSocketResponse, UrlDispatcher, Application

from dpl.model.domain_id import TDomainId
from dpl.api.http_api_provider import HttpApiProvider
from dpl.utils.observer import Observer
from dpl.auth.auth_context import AuthContext
from dpl.auth.auth_service import (
    AbsAuthService, AuthInvalidTokenError, ServiceEntityResolutionError
)
from dpl.events.event import Event
from dpl.events.object_related_event import ObjectRelatedEvent
from dpl.events.event_hub import EventHub
from dpl.api.api_errors import ERROR_TEMPLATES
from .receive_utils import own_receive_json
from .message import Message
from .message_json import message_dumps
from .message_utils import (
    build_message, parse_message
)
from .error_message_utlis import (
    send_error_message_by_code
)
from .subscription_storage import SubscriptionStorage
from .delivery_manager import DeliveryManager
from .streaming_flow_error import StreamingFlowError
from .error_handling_context import ErrorHandler

StreamingSessionData = Tuple[WebSocketResponse, asyncio.Task]
ActiveSessionsRegistry = Dict[TDomainId, StreamingSessionData]

LOGGER = logging.getLogger(__name__)


async def streaming_connection_handler(request: Request) -> WebSocketResponse:
    """
    This request handler handles incoming WebSockets connections and redirects
    their processing to corresponding functions

    :param request: a request to be handled
    :return: an instance of WebSocketResponse
    """
    ws = WebSocketResponse(heartbeat=60)
    await ws.prepare(request)

    app = request.app
    api_provider = app['api_provider']  # type: StreamingApiProvider

    try:
        async with ErrorHandler(ws_con=ws):
            await api_provider.handle_established_connection(ws)

    except Exception as exc:
        LOGGER.error(
            "Unhandled exception in Streaming API: %s", type(exc),
            exc_info=exc
        )

    return ws


class StreamingApiProvider(HttpApiProvider, Observer):
    """
    StreamingApiProvider implements handling of Streaming API logic. It handles
    attempts to establish WebSocket connection, Authentication flow, handling
    of incoming messages and sending system-side events
    """
    def __init__(
            self, auth_context: AuthContext, auth_service: AbsAuthService,
            api_root: str = '/',
            loop: asyncio.AbstractEventLoop = None
    ):
        """
        Constructor. Initializes internal data structures and saves references
        to the AuthContext and AbsAuthService

        :param auth_context: a reference to Authentication Context which saves
               information about the current Session for this Task or Thread
        :param auth_service: a reference to AuthService which allows to check
               access rights for different information in the system
        :param api_root: a path for the API root
        :param loop: event tool to be used for this provider
        """
        super().__init__(loop=loop)

        self._app['api_provider'] = weakref.proxy(self)
        self._app.on_shutdown.append(self.on_shutdown)
        self._auth_context = auth_context
        self._auth_service = auth_service
        self._subs_lock = asyncio.Lock(loop=self._loop)
        self._subs_storage = SubscriptionStorage()
        self._active_sessions = dict()  # type: ActiveSessionsRegistry
        self._active_sessions_lock = asyncio.Lock(loop=self._loop)
        self._delivery_manager = DeliveryManager(loop=self._loop)

        router = self._app.router  # type: UrlDispatcher
        router.add_get(path=api_root, handler=streaming_connection_handler)

    async def on_shutdown(self, app: Application) -> None:
        """
        Closes all opened sessions

        :param app: an instance of aiohttp Application which is shutting down
        :return: None
        """
        session_info_items = tuple(self._active_sessions.values())

        for ws, task in session_info_items:
            await ws.close(code=WSCloseCode.GOING_AWAY)
            await task

    async def invalidate_session(self, session_id: TDomainId) -> None:
        """
        Removes all session-related data from the internal storage and
        terminates current connection

        :param session_id: an identifier of Session to be invalidated
        :return: None
        """
        if session_id in self._active_sessions:
            ws, task = self._active_sessions[session_id]
            await send_error_message_by_code(
                ws=ws, error_code=2101
            )
            await ws.close()
            await task

        await self._subs_storage.remove_all_for(session_id)
        await self._delivery_manager.discard_for(session_id)

    async def handle_established_connection(self, ws: WebSocketResponse):
        """
        This function handles communication over WebSockets after the
        connection was established. It starts from authentication flow and then
        spins up a message handling loop

        :param ws: an instance of WebSocketResponse which represents WebSocket
               connection
        :return: None
        :raises AuthInvalidTokenError: if the specified access token was
                revoked or is not valid for some other reason
        """
        token = await self._handle_auth_flow(ws=ws)

        try:
            session = self._auth_service.view_current_session(
                access_token=token
            )
        except ServiceEntityResolutionError:
            raise AuthInvalidTokenError()

        session_id = session['domain_id']

        await self._register_session(session_id=session_id, ws=ws)

        auth_ack_message = build_message(
            type_="control",
            topic="auth_ack",
            body={}
        )

        # FIXME: CC41: Open the session explicitly in DeliveryManager

        try:
            ws.send_json(auth_ack_message, dumps=message_dumps)
            await self._message_loop(ws, session_id)
        finally:
            await self._cancel_session(session_id=session_id)

    def update(self, source: EventHub, *args, **kwargs) -> None:
        if not isinstance(source, EventHub):
            raise TypeError(
                "StreamingApiProvider can subscribe only on updates "
                "from EventHub instances"
            )

        event = kwargs.get('event', args[0])  # type: Event
        assert isinstance(event, Event)

        if isinstance(event, ObjectRelatedEvent):
            message_body = event.object_dto
        else:
            message_body = {}

        asyncio.ensure_future(
            self._send_data_to_all(event.timestamp, event.topic, message_body),
            loop=self._loop
        )

    async def _send_data_to_all(
            self, timestamp: float, topic: str, body: Mapping
    ) -> None:
        """
        Constructs the data message and sends it to all corresponding Clients

        :param timestamp: the time moment of message formation to be set
        :param topic: the topic of the message
        :param body: the content (payload) of the message
        :return: None
        """
        for session_id in self._subs_storage.list_sessions():
            is_retained = self._subs_storage.resolve_subscription_params(
                session_id=session_id, topic=topic
            )

            if is_retained is None:
                continue  # this Session is not subscribed to this message

            if is_retained or session_id in self._active_sessions:
                message = Message(
                    timestamp=timestamp, type_="data", topic=topic, body=body
                )

                await self._delivery_manager.put_message(
                    session_id=session_id, message=message,
                    ensure_delivery=is_retained
                )

    async def _handle_old_session(
            self, session_id: TDomainId,
            old_session_data: Tuple[WebSocketResponse, asyncio.Task],
    ) -> None:
        """
        Handles the situation when the old session is still open. Waits for the
        old connection to close or logs an error if it'll not be closed

        :param session_id: an identifier of the current session
        :param old_session_data: an information about the old session
        :return: None
        """
        LOGGER.error(
            "Session with such id is already present: %s",
            session_id
        )
        old_connection, old_task = old_session_data

        done, pending = await asyncio.wait(
            (old_task, asyncio.sleep(1, loop=self._loop)),
            return_when=asyncio.FIRST_COMPLETED, loop=self._loop
        )

        if old_task in done:
            LOGGER.debug(
                "Closing old session as not alive: %s", session_id
            )
            if old_task.exception():
                raise old_task.exception()
        else:
            LOGGER.error(
                "Old session was still alive, it will be closed: %s",
                session_id
            )
            await send_error_message_by_code(
                ws=old_connection, error_code=5004
            )
            await old_connection.close()
            await old_task

    async def _register_session(
            self, session_id: TDomainId, ws: WebSocketResponse
    ) -> None:
        """
        Removes Session from the registry of opened sessions

        :param session_id: an identifier of a Session to be registered
        :param ws: an instance of WebSocketResponse which represents WebSocket
               connection
        :return: None
        :raises
        """
        LOGGER.debug("Starting new streaming session: %s", session_id)

        current_task = asyncio.Task.current_task(loop=self._loop)

        async with self._active_sessions_lock:
            old_session_data = self._active_sessions.get(session_id)

        if old_session_data is not None:
            await self._handle_old_session(session_id, old_session_data)

        async with self._active_sessions_lock:
            await self._delivery_manager.resume_for(session_id)
            self._active_sessions[session_id] = ws, current_task

        LOGGER.debug("Streaming session started: %s", session_id)

    async def _cancel_session(
            self, session_id: TDomainId, code: int = 1000
    ) -> None:
        """
        Closes the session with the specified WebSocket close code
        and removes it from the list of opened sessions.

        :param session_id: an identifier of a Session to be registered
        :param code: a code to be passed to client in WS close message
        :return: None
        """
        LOGGER.debug("Closing streaming session: %s", session_id)

        async with self._active_sessions_lock:
            if session_id not in self._active_sessions:
                LOGGER.error(
                    "Session with such id isn't present: %s",
                    session_id
                )

            await self._delivery_manager.pause_for(session_id)
            ws, current_task = self._active_sessions[session_id]
            await ws.close(code=code)
            self._active_sessions.pop(session_id)

    async def _handle_subscription_message(
            self, message: Message, session_id: TDomainId
    ) -> None:
        """
        Handles the new request on topic subscription

        :param message: a message to be handled
        :param session_id: an identifier of the current Session
        :return: None
        :raises StreamingFlowError: if client violated the format of
                Subscription message body
        """
        target_topic = message.body.get('target_topic')
        retain_messages = message.body.get('retain_messages', False)

        LOGGER.debug(
            "Subscription request from %s: %s %s", session_id,
            target_topic, retain_messages
        )

        if not isinstance(target_topic, str):
            error = ERROR_TEMPLATES[5030].to_dict()
            error['devel_message'] %= (
                "target_topic is not a string"
            )
            raise StreamingFlowError(error_info=error)

        if not isinstance(retain_messages, bool):
            error = ERROR_TEMPLATES[5030].to_dict()
            error['devel_message'] %= (
                "retain_messages is not a boolean"
            )
            raise StreamingFlowError(error_info=error)

        async with self._subs_lock:
            self._subs_storage.add_subscription(
                session_id=session_id,
                topic=target_topic, is_retained=retain_messages
            )

        message = build_message(
            type_="control",
            topic="subscribe_ack",
            body={"target_topic": target_topic}
        )

        await self._delivery_manager.put_message(
            session_id=session_id, message=message
        )

    async def _handle_unsubscription_message(
            self, message: Message, session_id: TDomainId
    ) -> None:
        """
        Handles the new request on unsubscription from a topic

        :param message: a message to be handled
        :param session_id: an identifier of the current Session
        :return: None
        :raises StreamingFlowError: if client violated the format of
                Unsubscription message body
        """
        target_topic = message.body.get('target_topic')

        LOGGER.debug(
            "Unubscription request from %s: %s", session_id, target_topic
        )

        if not isinstance(target_topic, str):
            error = ERROR_TEMPLATES[5030].to_dict()
            error['devel_message'] %= (
                "target_topic is not a string"
            )
            raise StreamingFlowError(error_info=error)

        async with self._subs_lock:
            self._subs_storage.remove_subscription(
                session_id=session_id, topic=target_topic
            )

        message = build_message(
            type_="control",
            topic="unsubscribe_ack",
            body={"target_topic": target_topic}
        )

        await self._delivery_manager.put_message(
            session_id=session_id, message=message
        )

    async def _handle_delivery_ack(
            self, message: Message, session_id: TDomainId
    ) -> None:
        """
        Analyzes the received delivery_ack message and removes the
        corresponding message from the list of undelivered

        :param message: a received message
        :param session_id: an identifier of the current Session
        :return: None
        :raises StreamingFlowError: if client violated the format of
                message body
        """
        message_id = message.body['message_id']

        if not isinstance(message_id, int):
            error = ERROR_TEMPLATES[5030].to_dict()
            error['devel_message'] %= (
                "message_id is missing or is not an integer"
            )
            raise StreamingFlowError(error_info=error)

        await self._delivery_manager.ack_delivery(
            session_id=session_id, message_id=message_id
        )

    async def _handle_control_message(
            self, message: Message, session_id: TDomainId
    ) -> None:
        """
        Analyses the new Control message from a client and, if needed,
        adds the corresponding message to the queue of outcoming messages

        :param message: a message from a client to be analyzed
        :param session_id: an identifier of the current Session
        :return: None
        :raises StreamingFlowError: if client violated the format of
                message body
        """
        if message.topic == "subscribe":
            await self._handle_subscription_message(message, session_id)
        elif message.topic == "unsubscribe":
            await self._handle_unsubscription_message(message, session_id)
        elif message.topic == "delivery_ack":
            await self._handle_delivery_ack(message, session_id)
        else:
            LOGGER.warning(
                "Unhandled control message from %s, ignored:\n"
                "%s %s %s %s", session_id, message.timestamp, message.type,
                message.topic, message.body
            )

    async def _handle_incoming_message(
            self, message: Message, session_id: TDomainId
    ) -> None:
        """
        Analyses the new message from a client and, if needed, adds the new
        message to the queue of outcoming messages

        :param message: a message from a client to be analyzed
        :param session_id: an identifier of the current Session
        :return: None
        :raises StreamingFlowError: if client violated the format of
                message body
        """
        if message.type == "control":
            await self._handle_control_message(message, session_id)

        else:
            LOGGER.warning(
                "Unhandled message from %s, ignored:\n"
                "%s %s %s %s", session_id, message.timestamp, message.type,
                message.topic, message.body
            )

    async def _handle_outcoming_message(
            self, ws: WebSocketResponse, message: Message
    ) -> None:
        """
        Analyses the new message to be sent to a client and sends it if it's
        appropriate (i.e., for example, if the client have an access to read
        that message)

        :param ws: an instance of WebSocketResponse which represents WebSocket
               connection
        :param message: a message to be sent to the client
        :return: None
        """
        # FIXME: Check access rights here
        ws.send_json(data=message, dumps=message_dumps)

    async def _on_incoming_waiter_finished(
            self, task: asyncio.Task, session_id: TDomainId
    ) -> None:
        """
        A method to be executed if incoming_waiter_task finished its execution

        :param task: an instance of incoming_waiter_task
        :param session_id: an identifier of the current Streaming Session
        :return: None
        """

        exception = task.exception()

        if exception is not None:
            raise exception

        result = task.result()
        message = parse_message(result)

        await self._handle_incoming_message(
            message=message, session_id=session_id
        )

    async def _on_outcoming_waiter_finished(
            self, ws: WebSocketResponse, task: asyncio.Task
    ) -> None:
        """
        A method to be executed if outcoming_waiter_task finished its execution

        :param ws: an instance of WebSocketResponse which represents WebSocket
               connection
        :param task: an instance of outcoming_waiter_task
        :return: None
        """
        exception = task.exception()

        if exception is not None:
            raise exception

        result = task.result()

        await self._handle_outcoming_message(
            ws=ws, message=result
        )

    async def _message_loop(
            self, ws: WebSocketResponse, session_id: TDomainId
    ) -> None:
        """
        Is responsible for handling of all incoming messages from client and
        of all messages to be sent from server to client (except
        error messages)

        :param ws: an instance of WebSocketResponse which represents WebSocket
               connection
        :param session_id: an identifier of the current session
        :return: None
        """
        start_task = functools.partial(
            asyncio.ensure_future, loop=self._loop
        )
        get_message = functools.partial(
            self._delivery_manager.get_message,
            session_id=session_id
        )

        incoming_waiter_task = start_task(own_receive_json(ws))
        outcoming_waiter_task = start_task(get_message())

        try:
            while not ws.closed:
                done, pending = await asyncio.wait(
                    (incoming_waiter_task, outcoming_waiter_task),
                    return_when=asyncio.FIRST_COMPLETED,
                    loop=self._loop
                )

                if incoming_waiter_task in done:
                    await self._on_incoming_waiter_finished(
                        task=incoming_waiter_task, session_id=session_id
                    )

                    incoming_waiter_task = start_task(own_receive_json(ws))

                if outcoming_waiter_task in done:
                    await self._on_outcoming_waiter_finished(
                        ws=ws, task=outcoming_waiter_task
                    )

                    outcoming_waiter_task = start_task(get_message())

        finally:
            incoming_waiter_task.cancel()
            outcoming_waiter_task.cancel()

    async def _handle_auth_flow(self, ws: WebSocketResponse) -> str:
        """
        This method handles client authentication flow:

        - waits for an "auth" message from client;
        - checks message validity;
        - extracts auth token;
        - returns authentication toke to the caller

        :param ws: an instance of WebSocketResponse which represents WebSocket
               connection
        :return: an extracted authentication token
        :raises StreamingFlowError: if the content of a message was different
                from expected
        """
        raw_message = await own_receive_json(ws, timeout=20)
        parsed_message = parse_message(raw_message)

        if parsed_message.type != "control":
            error = ERROR_TEMPLATES[5010].to_dict()
            raise StreamingFlowError(error_info=error)

        if parsed_message.topic != "auth":
            error = ERROR_TEMPLATES[5020].to_dict()
            error['devel_message'] %= (
                "auth", parsed_message.topic
            )
            raise StreamingFlowError(error_info=error)

        token = parsed_message.body.get('access_token')

        if not isinstance(token, str):
            error = ERROR_TEMPLATES[5030].to_dict()
            error['devel_message'] %= (
                "access_token is missing or is not a string"
            )
            raise StreamingFlowError(error_info=error)

        return token
