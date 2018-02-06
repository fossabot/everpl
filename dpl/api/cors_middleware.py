from typing import Callable

from aiohttp import web


class CorsMiddleware(object):
    """
    CorsMiddleware is a class of callable objects that
    will be able to intercept all requests coming to
    server and to add a corresponding set of CORS
    headers if needed
    """
    def __init__(self, is_enabled: True, allowed_origin='*'):
        """
        Constructor. Performs configuration of CORS handling
        logic

        :param is_enabled: is CORS enabled
        :param allowed_origin: specify an origin (address
               of a resource) of requests for which it is
               allowed to access resources on this server
        """
        self._is_enabled = is_enabled
        self._allowed_origin = allowed_origin

    @web.middleware
    async def handle(self, request: web.Request, handler: Callable) -> web.Response:
        """
        This method is an actual aiohttp middleware method.
        Intercepts all incoming requests, passes them to
        the next handler (it can be an another middleware
        from the chain or an actual handler), adds CORS
        headers and returns the result.

        For more information about middlewares see
        https://docs.aiohttp.org/en/stable/web.html#middlewares

        :param request: request to be handled
        :param handler: next request handler in a chain
        :return: a response to the request
        """

        response = await handler(request)  # type: web.Response

        if self._is_enabled:
            self._modify_response(response)

        return response

    def _modify_response(self, response: web.Response) -> None:
        """
        Appends CORS headers to the specified response

        :param response: HTTP response to be altered
        :return: None
        """
        # Nginx Rules for CORS handling:
        # add_header 'Access-Control-Allow-Origin'   '*'                               always;
        # add_header 'Access-Control-Allow-Headers'  'Content-Type, Authorization'     always;
        # add_header 'Access-Control-Allow-Methods'  $sent_http_allow                  always;

        response.headers.update(
            {
                'Access-Control-Allow-Origin': self._allowed_origin,
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
        )

        allowed_methods = response.headers.get('Allow')

        if allowed_methods is not None:
            response.headers.add(
                key='Access-Control-Allow-Methods',
                value=allowed_methods
            )

