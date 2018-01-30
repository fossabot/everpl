# Include standard modules
from typing import Dict, List

# Include DPL modules
from . import exceptions
from dpl.auth import AuthManager

from dpl.services.service_exceptions import ServiceEntityResolutionError
from dpl.services.abs_placement_service import AbsPlacementService
from dpl.services.abs_thing_service import AbsThingService, ServiceTypeError


class ApiGateway(object):
    """
    ApiGateway is a class which validates requests that came, checks permissions
    and pass requests further to corresponding components (to execute some command
    of fetch information about a specific thing, for example)
    """
    def __init__(
            self, auth_manager: AuthManager,
            thing_service: AbsThingService,
            placement_service: AbsPlacementService
    ):
        self._am = auth_manager
        self._things = thing_service
        self._placements = placement_service

    def auth(self, username: str, password: str) -> str:
        """
        Authenticate user and receive corresponding access token

        :param username: username of the user
        :param password: password of the user
        :return: an access token to be used
        """
        # FIXME: auth_user can raise ValueError on fail. Set a more specific exception
        # and document it
        return self._am.auth_user(username, password)

    def _check_permission(self, token: str, requested_action):
        """
        Checks is specified action is permitted for this token

        :param token: access token to be checked
        :param requested_action: information about a requested action or permission
        :return: None
        :raises PermissionError: if this action is not permitted for this token
        """
        if not self._am.is_token_valid(token):
            raise exceptions.InvalidTokenError("Specified token was revoked or not-existing at all")

        if not self._am.is_token_grants(token, requested_action):
            raise exceptions.PermissionDeniedForTokenError("Specified token doesn't permit this action")

    def get_things(self, token: str) -> List[Dict]:
        """
        Receive a full list of data about things

        :param token: access token
        :return: a list of things data
        """
        self._check_permission(token, None)

        return self._things.view_all()

    def get_thing(self, token: str, thing_id: str) -> Dict:
        """
        Receive information about a specific thing

        :param token: access token
        :param thing_id: an ID of thing to be fetched
        :return: a dict with full information about the thing
        """
        self._check_permission(token, None)

        try:
            return self._things.view(thing_id)
        except ServiceEntityResolutionError as e:
            raise exceptions.ThingNotFoundError("Thing with the specified id was not found") from e

    # FIXME: CC2: Make this method a coroutine?
    # FIXME: Specify a return value type
    def send_command(self, token: str, thing_id: str, command: str, *args, **kwargs):
        """
        Sends a command to specific thing with specified arguments

        :param token: access token
        :param thing_id: and ID of thing that must receive a specified command
        :param command: command to execute
        :param args: arguments to send to command
        :param kwargs: keyword-based arguments to send to command
        :return: an some ID or handler of planned task
        """
        # FIXME: Check permission: Send commands to things
        # FIXME: CC13: Add permission checking for specific things
        self._check_permission(token, None)

        try:
            self._things.send_command(
                to_actuator_id=thing_id,
                command=command,
                command_args=kwargs
            )

        except ServiceTypeError as e:
            raise exceptions.CommandNotOnActuatorError(
                "Unable to send command to {0}. Commands can be passed "
                "only to actuators.".format(thing_id)
            ) from e

        except ServiceEntityResolutionError as e:
            raise exceptions.ThingNotFoundError("Thing with the specified id was not found") from e

        except Exception as e:
            raise exceptions.CommandFailedError() from e

        # FIXME: Return Task, Task ID or just remove this line
        return None

    # FIXME: Specify a return value type
    def get_task_status(self, token: str, task_id):
        """
        Get a status of a planned task

        :param token: an access token
        :param task_id: some id or handler of task to be fetched
        :return: a status of the task
        """
        raise NotImplementedError()

    def get_placements(self, token: str) -> List[Dict]:
        """
        Returns a list of dict-like representations of all placements

        :param token: access token
        :return: a list of placements data
        """
        # FIXME: Check permission: View placements
        self._check_permission(token, None)

        return self._placements.view_all()

    def get_placement(self, token: str, placement_id: str) -> Dict:
        """
        Returns a dict-like representation of placement with the specified ID

        :param token: access token
        :param placement_id: an ID of placement to be fetched
        :return: a dict with full information about the placement
        """
        # FIXME: Check permission: View placements
        self._check_permission(token, None)

        try:
            return self._placements.view(placement_id)
        except ServiceEntityResolutionError as e:
            raise exceptions.PlacementNotFoundError("The placement with the specified ID was not found") from e

    # TODO: Add a method to provide access to push-notifications on system events
    # like changed status of a thing (for example, but not limited to)

