"""
This module contains a definition of an ErrorHandler - asynchronous context
manager which handles standard errors raised by Streaming API methods and
sends corresponding messages to the Clients.
"""

import asyncio
import json
import functools
import time

from aiohttp.web import WebSocketResponse

from dpl.auth.exceptions import AuthInvalidTokenError
from dpl.api.api_errors import ERROR_TEMPLATES
from .error_message_utlis import send_error_message_by_code, send_error_message
from .message import MessageFormatViolationError
from .receive_utils import NotTextFrame
from .streaming_flow_error import StreamingFlowError


class ErrorHandler(object):
    """
    ErrorHandler is an asynchronous context manager which handles exceptions
    raised by streaming APIs, sends corresponding error messages to Clients
    and finally closes WebSocket connection
    """
    def __init__(self, ws_con: WebSocketResponse):
        """
        Constructor. Saves an instance of WebSocketResponse for communication
        via WebSocket connection

        :param ws_con: an instance of WebSocketResponse for communication
               via WebSocket connection
        """
        self._ws_con = ws_con

    async def __aenter__(self):
        """
        Entering the context. Does nothing

        :return: None
        """
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exiting from the context. Handles all known exceptions and
        closes connection at the end

        :param exc_type: type of the raised exception
        :param exc_val: instance of the raised exception
        :param exc_tb: exception traceback
        :return: falsable statement if exception wasn't handled,
                 truable otherwise
        """
        exc_handled = await _handle_exception(
            exc_val, exc_tb=exc_tb,
            ws_con=self._ws_con
        )

        await self._ws_con.close()

        return exc_handled


@functools.singledispatch
async def _handle_exception(exc_val, exc_tb, ws_con) -> bool:
    """
    Handles exception raised inside the context of a context manager

    :param exc_val: instance of the raised exception
    :param exc_tb: exception traceback
    :return: True if the exception was handled, False otherwise
    """
    return False  # don't handle exceptions by default


@_handle_exception.register(asyncio.CancelledError)
@_handle_exception.register(asyncio.TimeoutError)
async def _(exc_val, exc_tb, ws_con):
    await send_error_message_by_code(ws=ws_con, error_code=5000)
    return True


@_handle_exception.register(MessageFormatViolationError)
async def _(exc_val, exc_tb, ws_con):
    await send_error_message_by_code(
        ws=ws_con, error_code=5003, format_params=(
            exc_val.violated_field, exc_val.expected, exc_val.received
        )
    )
    return True


@_handle_exception.register(asyncio.TimeoutError)
async def _(exc_val, exc_tb, ws_con):
    await send_error_message_by_code(ws=ws_con, error_code=5000)
    return True


@_handle_exception.register(NotTextFrame)
async def _(exc_val, exc_tb, ws_con):
    await send_error_message_by_code(ws=ws_con, error_code=5001)
    return True


@_handle_exception.register(json.JSONDecodeError)
async def _(exc_val, exc_tb, ws_con):
    await send_error_message_by_code(ws=ws_con, error_code=5002)
    return True


@_handle_exception.register(StreamingFlowError)
async def _(exc_val, exc_tb, ws_con):
    await send_error_message(
        ws=ws_con, error_info=exc_val.error_info
    )
    return True


@_handle_exception.register(AuthInvalidTokenError)
async def _(exc_val, exc_tb, ws_con):
    await send_error_message_by_code(ws=ws_con, error_code=2101)
    return True


@_handle_exception.register(Exception)
async def _(exc_val, exc_tb, ws_con):
    error = ERROR_TEMPLATES[1003].to_dict()
    now = time.time()
    error['user_message'] = error['user_message'].format(timestamp=now)

    await send_error_message(ws=ws_con, error_info=error)

    return False
