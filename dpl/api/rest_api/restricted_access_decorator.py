"""
This module contains a definition of a restricted_access_decorator
"""
import functools

import aiohttp.web as web

from dpl.auth.auth_context import AuthContext
from dpl.auth.exceptions import AuthInvalidTokenError
from dpl.api.api_errors import ERROR_TEMPLATES
from .common import RequestHandlerType, make_json_response


def restricted_access(wrapped: RequestHandlerType) -> RequestHandlerType:
    """
    A decorator which wraps the specified callable (request
    handler coroutine) with an auth-handling logic

    :param wrapped: a request handler to be wrapped
    :return: a request handler with an additional auth logic
    """
    @functools.wraps(wrapped)
    async def _auth_wrapper(request: web.Request) -> web.Response:
        """
        This wrapper extracts an access token from a request
        headers, extracts an instance of AuthContext from
        a related aiohttp Application, passes an execution
        to the real request handler and handles auth-related
        errors

        :param request: an HTTP request to be handled
        :return: a response to the HTTP request
        """
        headers = request.headers  # type: dict

        token = headers.get("Authorization", None)

        if token is None:
            return make_json_response(
                status=401,
                content=ERROR_TEMPLATES[2100].to_dict()
            )

        try:
            auth_context = request.app['auth_context']  # type: AuthContext
            assert isinstance(auth_context, AuthContext)

            with auth_context(token=token):
                return await wrapped(request)

        except AuthInvalidTokenError:
            error_dict = ERROR_TEMPLATES[2101].to_dict()

            return make_json_response(
                status=401,
                content=error_dict
            )

    return _auth_wrapper
