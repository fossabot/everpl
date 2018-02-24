import json
import functools
from typing import Callable, Awaitable

import aiohttp.web as web

from dpl.api.api_errors import ERROR_TEMPLATES
from .common import CONTENT_TYPE_JSON, make_json_response


RequestHandlerType = Callable[[web.Request], Awaitable[web.Response]]


def json_decode_decorator(decorated: RequestHandlerType) -> RequestHandlerType:
    """
    This decorator allows to decorate web requests handlers
    for Content-Type HTTP header checking and processing of
    JSON decoding errors

    :param decorated: a web request handler to be decorated
    :return: a wrapper function which implements a request
             checking logic
    """
    @functools.wraps(decorated)
    async def _wrapper(request: web.Request) -> web.Response:
        if request.content_type != CONTENT_TYPE_JSON:
            return make_json_response(
                status=400,
                content=ERROR_TEMPLATES[1000].to_dict()
            )

        try:
            result = await decorated(request)
        except json.JSONDecodeError:
            return make_json_response(
                status=400,
                content=ERROR_TEMPLATES[1001].to_dict()
            )

        return result

    return _wrapper

