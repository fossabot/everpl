"""
This module contains utility functions for sending of Streaming Error Messages
"""
from typing import Mapping

from aiohttp.web import WebSocketResponse

from dpl.api.api_errors import ERROR_TEMPLATES
from .message import Message
from .message_utils import build_message
from .message_json import message_dumps


def build_error_message(body: Mapping) -> Message:
    """
    This utility method just constructs error messages to be sent by
    Streaming API

    :param body: the body of the message (error definition)
    :return: the constructed message
    """
    message = build_message(
        type_="control",
        topic="error",
        body=body
    )

    return message


async def send_error_message(
        ws: WebSocketResponse, error_info: Mapping, format_params=None
) -> None:
    """
    This utility method allows to send an Error Message to the client with
    the specified information about an error and optional string formatting

    :param ws: an instance of WebSocketResponse which represents WebSocket
           connection
    :param error_info: information about an error
    :param format_params: optional parameters used for string formatting
           of the devel_message field
    :return: None
    """
    if format_params:
        error_info['devel_message'] %= format_params

    message = build_error_message(
        body=error_info
    )

    ws.send_json(message, dumps=message_dumps)


async def send_error_message_by_code(
        ws: WebSocketResponse, error_code: int, format_params=None
) -> None:
    """
    An alternative to the send_error_message which constructs the whole
    error message based on the specified error code

    :param ws: an instance of WebSocketResponse which represents WebSocket
           connection
    :param error_code: a code of the error to be sent
    :param format_params: optional parameters used for string formatting
           of the devel_message field
    :return: None
    """
    error_template = ERROR_TEMPLATES[error_code].to_dict()

    await send_error_message(
        ws=ws, error_info=error_template, format_params=format_params
    )
