"""
This module contains definitions of an aiohttp
application controlling the /placements/ route
"""
from typing import Mapping

import aiohttp.web as web
from dpl.utils.empty_mapping import EMPTY_MAPPING

from dpl.services.abs_placement_service import (
    AbsPlacementService,
    ServiceEntityResolutionError
)
from dpl.auth.exceptions import AuthInsufficientPrivilegesError
from dpl.api.api_errors import ERROR_TEMPLATES
from .common import make_json_response
from .restricted_access_decorator import restricted_access


def build_placements_subapp(
        placement_service: AbsPlacementService,
        additional_data: Mapping = EMPTY_MAPPING
) -> web.Application:
    """
    A factory of aiohttp's Applications. Initializes and returns
    an Application for managing of Placements

    :param placement_service: an instance of thing_service used
           for managing of Placements
    :param additional_data: additional data to be saved in app's
           context (data store)
    :return: an instance of aiohttp Application
    """
    app = web.Application()
    app['placement_service'] = placement_service
    app.update(additional_data)
    router = app.router

    router.add_get(path='/', handler=placements_get_handler)
    router.add_route(method='OPTIONS', path='/', handler=placements_options_handler)
    router.add_get(path='/{id}', handler=placement_get_handler)
    router.add_route(method='OPTIONS', path='/{id}', handler=placement_options_handler)

    return app


@restricted_access
async def placements_get_handler(request: web.Request) -> web.Response:
    """
    A handler for GET requests for path /placements/

    :param request: request to be processed
    :return: a response to request
    """
    placement_service = request.app['placement_service']  # type: AbsPlacementService

    try:
        return make_json_response(
            {"placements": placement_service.view_all()}
        )
    except AuthInsufficientPrivilegesError:
        error_dict = ERROR_TEMPLATES[2110].to_dict()

        error_dict["user_message"] = error_dict["user_message"].format(action="viewing of placements data")

        return make_json_response(
            status=403,
            content=error_dict
        )


async def placements_options_handler(request: web.Request) -> web.Response:
    """
    A handler for OPTIONS request for path /placements/.

    Returns a response that contains 'Allow' header with all allowed HTTP methods.

    :param request: request to be handled
    :return: a response to request
    """
    return web.Response(
        body=None,
        status=204,
        headers={'Allow': 'GET, HEAD, OPTIONS'}
    )


def _get_placement_id(request: web.Request) -> str:
    placement_id = request.match_info['id']

    return placement_id


@restricted_access
async def placement_get_handler(request: web.Request) -> web.Response:
    """
    A handler for GET requests for path /placements/{id}

    :param request: request to be processed
    :return: a response to request
    """
    placement_id = _get_placement_id(request)
    placement_service = request.app['placement_service']  # type: AbsPlacementService

    try:
        return make_json_response(placement_service.view(placement_id))

    except ServiceEntityResolutionError:
        return make_json_response(
            status=404,
            content=ERROR_TEMPLATES[1005].to_dict()
        )

    except AuthInsufficientPrivilegesError:
        error_dict = ERROR_TEMPLATES[2110].to_dict()

        error_dict["user_message"] = error_dict["user_message"].format(action="viewing of placements data")

        return make_json_response(
            status=403,
            content=error_dict
        )


async def placement_options_handler(request: web.Request) -> web.Response:
    """
    A handler for OPTIONS request for path /placements/{id}.

    Returns a response that contains 'Allow' header with all allowed HTTP methods.

    :param request: request to be handled
    :return: a response to request
    """
    return web.Response(
        body=None,
        status=204,
        headers={'Allow': 'GET, HEAD, OPTIONS'}
    )
