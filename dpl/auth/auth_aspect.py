"""
This module contains a definition of authorization aspect -
a factory of interceptor methods which will intercept original
calls, extract an access token and other contextual information,
check user authentication using AuthService.check_permission
method and only then will pass execution to the wrapped method
"""
import inspect
import functools
from typing import Callable

from .exceptions import AuthMissingTokenError
from .abs_auth_service import AbsAuthService
from .auth_context import AuthContext


class AuthAspect(object):
    """
    A callable factory class that contains a definition of
    an authorization advice. Such advice contains a logic
    of extracting of contextual information (like an access
    token, name of the domain / requested service and
    requested action / service method) and checking it with
    AuthService.check_permission functionality.
    """
    def __init__(self, auth_service: AbsAuthService, auth_context: AuthContext):
        """
        Constructor. Accepts an instance of AuthService used
        for permission checking and an instance of AuthContext
        for extraction of an access token

        :param auth_service: an instance of AuthService,
               an object that will be used for permission
               (authorization) checking
        :param auth_context: an instance of AuthContext, an
               object that will be used for extraction of
               contextual information and access token in
               particular
        """
        self._auth_service = auth_service
        self._auth_context = auth_context

    def __call__(self, wrapped_f: Callable) -> Callable:
        """
        Returns a new callable which wraps the specified
        wrapped_f callable with authorization logic

        :param wrapped_f: a callable to be wrapped
        :return: a new callable which wraps the specified one
        """
        original_wrapped = inspect.unwrap(wrapped_f)
        qualname = original_wrapped.__qualname__  # type: str

        domain, method_name = qualname.rsplit(sep='.', maxsplit=1)

        @functools.wraps(wrapped_f)
        def _auth_advice(*args, **kwargs):
            """
            An authorization advice. Checks if the access token
            associated with a current authorization context permits
            execution of the requested action in the specified domain
            with the specified arguments and, if everything is OK,
            passes control to the wrapped (requested) method.

            :param args: positional arguments to be passed to the
                   wrapped callable
            :param kwargs: keyword arguments to be passed to the
                   wrapped callable
            :return: the same value as was returned by the wrapped
                     callable
            :raises: the same exceptions as was raised by the wrapped
                     callable
            :raises AuthMissingTokenError: if there is no access token
                    saved in the current context
            """
            token = self._auth_context.current_token

            if token is None:
                raise AuthMissingTokenError(
                    "Denied access to a protected service: Method was "
                    "called outside of an Authorization Context?"
                )

            self._auth_service.check_permission(
                access_token=token,
                in_domain=domain,
                to_execute=method_name,
                args=args,
                kwargs=kwargs
            )

            return wrapped_f(*args, **kwargs)

        return _auth_advice
