# Include standard modules
from typing import Dict, List

# Include 3rd-party modules

# Include DPL modules
from adpl.auth import AuthManager
from .dummy_things_example import DUMMY_THINGS_EXAMPLE


class ApiGateway(object):
    """
    ApiGateway is a class which validates requests that came, checks permissions
    and pass requests further to corresponding components (to execute some command
    of fetch information about a specific thing, for example)
    """
    def __init__(self, auth_manager: AuthManager):
        self._am = auth_manager

    def auth(self, username: str, password: str) -> str:
        """
        Authenticate user and receive corresponding access token
        :param username: username of the user
        :param password: password of the user
        :return: an access token to be used
        """
        return self._am.auth_user(username, password)

    def get_things(self, token: str) -> List[Dict]:
        """
        Receive a full list of data about things
        :param token: access token
        :return: a list of things data
        """
        if self._am.is_token_grants(token, None):
            return DUMMY_THINGS_EXAMPLE
        else:
            raise PermissionError("Specified token doesn't permit this action")

    def get_thing(self, token: str, thing_id: str) -> Dict:
        """
        Receive information about a specific thing
        :param token: access token
        :param thing_id: an ID of thing to be fetched
        :return: a dict with full information about the thing
        """
        # FIXME: Remove brute-force search
        for thing in self.get_things(token):
            if thing.get('id') == thing_id:
                return thing

        raise ValueError("Thing with the specified id is not found")

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
        raise NotImplementedError

    # FIXME: Specify a return value type
    def get_task_status(self, token: str, task_id):
        """
        Get a status of a planned task
        :param token: an access token
        :param task_id: some id or handler of task to be fetched
        :return: a status of the task
        """
        raise NotImplementedError

    # TODO: Add a method to provide access to push-notifications on system events
    # like changed status of a thing (for example, but not limited to)

