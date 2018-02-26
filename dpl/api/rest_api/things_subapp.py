"""
This module contains definitions of an aiohttp
application controlling the /things/ route
"""
from typing import Mapping

import aiohttp.web as web
from dpl.utils import filtering
from dpl.utils.empty_mapping import EMPTY_MAPPING

from dpl.auth.exceptions import (
    AuthInsufficientPrivilegesError
)
from dpl.services.abs_thing_service import (
    AbsThingService,
    ServiceEntityResolutionError,
    ServiceTypeError,
    ServiceInvalidArgumentsError
)
from dpl.api.api_errors import ERROR_TEMPLATES

from .common import make_json_response
from .restricted_access_decorator import restricted_access
from .json_decode_decorator import json_decode_decorator


def build_things_subapp(
        thing_service: AbsThingService,
        additional_data: Mapping = EMPTY_MAPPING
) -> web.Application:
    """
    A factory of aiohttp's Applications. Initializes and returns
    an Application for managing of Things

    :param thing_service: an instance of thing_service used for
           managing of Things
    :param additional_data: additional data to be saved in app's
           context (data store)
    :return: an instance of aiohttp Application
    """
    app = web.Application()
    app['thing_service'] = thing_service
    app.update(additional_data)
    router = app.router

    router.add_get(path='/', handler=things_get_handler)
    router.add_route(method='OPTIONS', path='/', handler=things_options_handler)
    router.add_get(path='/{id}', handler=thing_get_handler)
    router.add_route(method='OPTIONS', path='/{id}', handler=thing_options_handler)

    return app


@restricted_access
async def things_get_handler(request: web.Request) -> web.Response:
    """
    A handler for GET requests for path /things/

    :param request: request to be processed
    :return: a response to request
    """
    thing_service = request.app['thing_service']

    try:
        query_params = request.query

        if 'placement' in query_params:
            things = thing_service.select_by_placement(
                query_params['placement']
            )
        else:
            things = thing_service.view_all()

        if 'type' in query_params:
            things = filtering.filter_items(
                things,
                {'type': query_params['type']}
            )

        return make_json_response({"things": things})

    except AuthInsufficientPrivilegesError:
        error_dict = ERROR_TEMPLATES[2110].to_dict()

        error_dict["user_message"] = error_dict["user_message"].format(action="viewing of things data")

        return make_json_response(
            status=403,
            content=error_dict
        )


async def things_options_handler(request: web.Request) -> web.Response:
    """
    A handler for OPTIONS request for path /things/.

    Returns a response that contains 'Allow' header with all allowed HTTP methods.

    :param request: request to be handled
    :return: a response to request
    """
    return web.Response(
        body=None,
        status=204,
        headers={'Allow': 'GET, HEAD, OPTIONS'}
    )


def _get_thing_id(request: web.Request) -> str:
    thing_id = request.match_info['id']

    return thing_id


@restricted_access
async def thing_get_handler(request: web.Request) -> web.Response:
    """
    A handler for GET requests for path /things/{id}

    :param request: request to be processed
    :return: a response to request
    """
    thing_id = _get_thing_id(request)
    thing_service = request.app['thing_service']

    try:
        thing = thing_service.view(thing_id)

        return make_json_response(thing)

    except ServiceEntityResolutionError:
        return make_json_response(
            status=404,
            content=ERROR_TEMPLATES[1005].to_dict()
        )

    except AuthInsufficientPrivilegesError:
        error_dict = ERROR_TEMPLATES[2110].to_dict()

        error_dict["user_message"] = error_dict["user_message"].format(action="viewing of things data")

        return make_json_response(
            status=403,
            content=error_dict
        )


async def thing_options_handler(request: web.Request) -> web.Response:
    """
    A handler for OPTIONS request for path /things/{id}.

    Returns a response that contains 'Allow' header with all allowed HTTP methods.

    :param request: request to be handled
    :return: a response to request
    """
    return web.Response(
        body=None,
        status=204,
        headers={'Allow': 'GET, HEAD, OPTIONS'}
    )


@restricted_access
@json_decode_decorator
async def thing_execute_post_handler(request: web.Request) -> web.Response:
    """
    A handler for POST requests to the /things/{id}/execute
    endpoint. Processes request on command execution for
    actuators

    :param request: request to be handled
    :return: a response to request
    """
    thing_id = _get_thing_id(request)
    thing_service = request.app['thing_service']  # type: AbsThingService

    payload = await request.json()
    command = payload.get('command')
    command_args = payload.get('command_args')

    if not isinstance(command, str):
        return make_json_response(
            status=400,
            content=ERROR_TEMPLATES[3101].to_dict()
        )

    if not isinstance(command_args, Mapping):
        return make_json_response(
            status=400,
            content=ERROR_TEMPLATES[3102].to_dict()
        )

    try:
        thing_service.send_command(
            to_actuator_id=thing_id,
            command=command,
            command_args=command_args
        )

        return make_json_response(
            content={"message": "accepted"},
            status=202
        )

    except ServiceEntityResolutionError:
        return make_json_response(
            status=404,
            content=ERROR_TEMPLATES[1005].to_dict()
        )

    except AuthInsufficientPrivilegesError:
        error_dict = ERROR_TEMPLATES[2110].to_dict()

        error_dict["user_message"] = error_dict["user_message"].format(
            action="sending commands to Actuators"
        )

        return make_json_response(
            status=403,
            content=error_dict
        )

    except ServiceTypeError:
        return make_json_response(
            status=404,
            content=ERROR_TEMPLATES[3100].to_dict()
        )

    except ServiceInvalidArgumentsError:
        return make_json_response(
            status=400,
            content=ERROR_TEMPLATES[3103].to_dict()
        )

