import warnings
from typing import Mapping

import aiohttp.web as web
from dpl.utils.empty_mapping import EMPTY_MAPPING

from dpl.services.abs_thing_service import (
    AbsThingService,
    ServiceTypeError,
    ServiceEntityResolutionError
)
from dpl.auth.exceptions import AuthInsufficientPrivilegesError

from .json_decode_decorator import json_decode_decorator
from .restricted_access_decorator import restricted_access
from .common import (
    make_json_response
)


def make_error_response(message: str, status: int = 400) -> web.Response:
    """
    Creates a simple JSON response with specified error code and explanatory message
    :param message: explanatory message
    :param status: status code of the response
    :return: created response
    """
    return make_json_response(
        content={"status": status, "message": message},
        status=status
    )


def build_messages_subapp(
        thing_service: AbsThingService,
        additional_data: Mapping = EMPTY_MAPPING
) -> web.Application:
    """
    A factory of aiohttp's Applications. Initializes and returns
    an Application for sending of commands to Actuators

    :param thing_service: an instance of thing_service used
          for managing of Things
    :param additional_data: additional data to be saved in app's
           context (data store)
    :return: an instance of aiohttp Application
    """
    warnings.warn(
        "The /messages/ route will be removed in v0.3",
        PendingDeprecationWarning
    )

    app = web.Application()
    app['thing_service'] = thing_service
    app.update(additional_data)
    router = app.router

    router.add_post(path='/', handler=messages_post_handler)
    router.add_route(method='OPTIONS', path='/', handler=messages_options_handler)

    return app


@restricted_access
@json_decode_decorator
async def messages_post_handler(request: web.Request) -> web.Response:
    """
    ONLY FOR COMPATIBILITY: Accept 'action requested' messages from clients.
    Handle POST requests for /messages/ path.

    :param request: request to be processed
    :return: a response to request
    """
    warnings.warn(
        "/messages/ path is deprecated. Use /things/{id}/execute endpoint instead",
        PendingDeprecationWarning
    )

    request_body = await request.json()

    msg_type = request_body.get("type", None)

    if msg_type is None:
        return make_error_response(status=400, message="Invalid message format: missing 'type' value")

    if msg_type != "user_request":
        return make_error_response(
            status=400,
            message="Unsupported message type: {0}. "
                    "Only type='user_request' is supported".format(msg_type)
        )

    msg_event = request_body.get("event", None)

    if msg_event != "action_requested":
        return make_error_response(
            status=400,
            message="Unsupported event specified: {0}. "
                    "Only event='action_requested' is supported".format(msg_event)
        )

    msg_body = request_body.get("body", None)  # type: dict

    if not isinstance(msg_body, dict):
        return make_error_response(
            status=400,
            message="Message body is invalid or absent."
        )

    # TODO: Consider consolidation of error messages and adding of link to knowledge base

    thing_action = msg_body.get("action", None)  # type: str

    if thing_action is None:
        return make_error_response(
            status=400,
            message="Requested action is not specified in message body or is null."
        )

    thing_id = msg_body.get("obj_id", None)  # type: str

    if thing_id is None:
        return make_error_response(
            status=400,
            message="obj_id (unique identifier of specific Thing)"
                    "is not specified or is null."
        )

    thing_action_params = msg_body.get("action_params", None)  # type: dict

    if not isinstance(thing_action_params, dict):
        return make_error_response(
            status=400,
            message="A value of action_params is invalid or absent."
                    "It must be a dictionary that contains all parameters"
                    "that need to be passed to thing to perform the specified action."
        )

    thing_service = request.app['thing_service']

    try:
        thing_service.send_command(
            to_actuator_id=thing_id,
            command=thing_action,
            command_args=thing_action_params
        )
    except AuthInsufficientPrivilegesError:
        return make_error_response(
            status=403,
            message="You are not authorized to process this action"
        )

    except ServiceEntityResolutionError:
        return make_error_response(
            status=400,
            message="Requested Thing is not existing"
        )

    except ServiceTypeError:
        return make_error_response(
            status=400,
            message="Requested to send a command to a non-actuator Thing"
        )

    return make_json_response(
        content={"message": "accepted"},
        status=202
    )


async def messages_options_handler(request: web.Request) -> web.Response:
    """
    A handler for OPTIONS request for path /messages/.

    Returns a response that contains 'Allow' header with all allowed HTTP methods.

    :param request: request to be handled
    :return: a response to request
    """
    return web.Response(
        body=None,
        status=204,
        headers={'Allow': 'POST, HEAD, OPTIONS'}
    )
