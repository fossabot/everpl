"""
This module contains utility functions and definitions which are useful for
receiving and processing WebSocket messages
"""
import json

from aiohttp.web import WebSocketResponse, WSMsgType


class NotTextFrame(Exception):
    """
    An exception to be raised if the client sent a frame that is not a TEXT
    frame
    """
    pass


async def own_receive_json(
        ws: WebSocketResponse, *, loads=json.loads, timeout: int = None
):
    """
    This coroutine emulates the behaviour of a receive_json method of
    WebSocketResponse. In difference to the original method, a NotTextFrame
    error is raised instead of generic TypeError.

    :param ws: an instance of WebSocketResponse used for message receiving
    :param loads: any callable that accepts str and returns dict with parsed
           JSON (json.loads() by default).
    :param timeout: timeout for receive operation.
    :return: loaded JSON content
    :raises NotTextFrame: if message is not TEXT.
    :raises json.JSONDecodeError: if message is not valid JSON.
    """
    frame = await ws.receive(timeout=timeout)

    if frame.type == WSMsgType.TEXT:
        return loads(frame.data)
    else:
        raise NotTextFrame()
