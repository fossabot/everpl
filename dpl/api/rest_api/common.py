"""
This module contains some utility methods and definitions
which are commonly used by request handlers
"""
import json
import warnings

from typing import Callable, Awaitable

import aiohttp.web as web

from dpl.utils.json_enum_encoder import JsonEnumEncoder


# Declare an alias for request handler type
RequestHandlerType = Callable[[web.Request], Awaitable[web.Response]]

# Declare constants:
CONTENT_TYPE_JSON = "application/json"


def make_error_response(message: str, status: int = 400) -> web.Response:
    """
    Creates a simple JSON response with specified error code and explanatory message
    :param message: explanatory message
    :param status: status code of the response
    :return: created response
    """
    warnings.warn(DeprecationWarning)

    return make_json_response(
        content={"status": status, "message": message},
        status=status
    )


def make_json_response(content: dict, status: int = 200) -> web.Response:
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
