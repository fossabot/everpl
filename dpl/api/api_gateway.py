# Include standard modules
from typing import Dict, List

# Include 3rd-party modules
import warnings

# Include DPL modules
from . import exceptions
from dpl.auth import AuthManager
from dpl.integrations import BindingManager
from dpl.placements import Placement, PlacementManager
from dpl.utils import obj_to_dict
from dpl.things import Thing, Actuator


class ApiGateway(object):
    """
    ApiGateway is a class which validates requests that came, checks permissions
    and pass requests further to corresponding components (to execute some command
    of fetch information about a specific thing, for example)
    """
    def __init__(self, auth_manager: AuthManager, binding_manager: BindingManager, placement_manager: PlacementManager):
        self._am = auth_manager
        self._bm = binding_manager
        self._placements = placement_manager

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

    def _thing_to_dict(self, thing: Thing) -> dict:
        """
        Just convert a thing object to a corresponding dict.

        In addition to simple object -> dict serialization, the content of 'metadata'
        property will be moved to resulting dict body.

        :param thing: an instance of Thing to be converted
        :return: a corresponding dict
        """
        thing_dict = obj_to_dict(thing)
        metadata = thing_dict.pop("metadata")
        assert isinstance(metadata, dict)

        thing_dict.update(**metadata)

        return thing_dict

    def _thing_to_dict_legacy(self, thing: Thing) -> dict:
        """
        Convert a thing object to a corresponding dict representation that is compatible
        to the legacy API

        :param thing: an instance of Thing to be converted
        :return: a corresponding dict
        """
        warnings.warn("Legacy representation of things will be dropped in the next release"
                      "of this platform. Please, switch to the '_thing_to_dict' method usage",
                      PendingDeprecationWarning)

        thing_dict = self._thing_to_dict(thing)
        thing_dict['description'] = thing_dict['friendly_name']

        return thing_dict

    def get_things(self, token: str) -> List[Dict]:
        """
        Receive a full list of data about things

        :param token: access token
        :return: a list of things data
        """
        self._check_permission(token, None)

        result = list()
        things = self._bm.fetch_all_things()

        for thing in things:
            result.append(self._thing_to_dict_legacy(thing))

        return result

    def _get_thing(self, token: str, thing_id: str) -> Thing:
        """
        Private method. Receive an instance of a specific thing

        :param token: access token
        :param thing_id: an ID of thing to be fetched
        :return: an instance of Thing that is related to the specified ID
        """
        # Check permission on viewing thing
        self._check_permission(token, None)

        try:
            thing = self._bm.fetch_thing(thing_id)
        except KeyError as e:
            raise exceptions.ThingNotFoundError("Thing with the specified id was not found") from e

        return thing

    def get_thing(self, token: str, thing_id: str) -> Dict:
        """
        Receive information about a specific thing

        :param token: access token
        :param thing_id: an ID of thing to be fetched
        :return: a dict with full information about the thing
        """
        # Permission on viewing of thing must be checked in '_get_thing' method
        # self._check_permission(token, None)

        thing = self._get_thing(token, thing_id)

        return self._thing_to_dict_legacy(thing)

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

        thing = self._get_thing(token, thing_id)  # type: Actuator

        if not isinstance(thing, Actuator):
            raise exceptions.CommandNotOnActuatorError(
                "Unable to send command to {0}. Commands can be passed "
                "only to actuators.".format(thing_id)
            )

        # Send command on execution. It can raise an exception too!
        try:
            thing.execute(command, *args, **kwargs)
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
        raise NotImplementedError

    @classmethod
    def _placement_to_dict(cls, placement: Placement) -> Dict:
        """
        Converts an instance of Placement to corresponding dictionary

        :return: a dictionary with all properties of placement
        """
        # FIXME: CC14: Consider switching to direct usage of properties
        return {
            "id": placement.placement_id,
            "friendly_name": placement.friendly_name,
            "image_url": placement.image_url
        }

    @classmethod
    def _placement_to_dict_legacy(cls, placement: Placement) -> Dict:
        """
        Converts an instance of Placement to corresponding dictionary that is compatible
        with the legacy API ('description' field will be set to the value of 'friendly_name' field,
        'image' field will be set to a value of 'image_url' field).

        :return: a dictionary with all properties of placement
        """
        warnings.warn("Legacy representation of placements will be dropped in the next release"
                      "of this platform. Please, switch to the '_placement_to_dict' method",
                      PendingDeprecationWarning)

        result = ApiGateway._placement_to_dict(placement)

        result["description"] = placement.friendly_name
        result["image"] = placement.image_url

        return result

    def get_placements(self, token: str) -> List[Dict]:
        """
        Returns a list of dict-like representations of all placements

        :param token: access token
        :return: a list of placements data
        """
        # FIXME: Check permission: View placements
        self._check_permission(token, None)

        result = list()

        for placement in self._placements.fetch_all_placements():
            result.append(self._placement_to_dict_legacy(placement))

        return result

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
            placement = self._placements.fetch_placement(placement_id)
        except KeyError as e:
            raise exceptions.PlacementNotFoundError("The placement with the specified ID was not found") from e

        return self._placement_to_dict_legacy(placement)


    # TODO: Add a method to provide access to push-notifications on system events
    # like changed status of a thing (for example, but not limited to)

