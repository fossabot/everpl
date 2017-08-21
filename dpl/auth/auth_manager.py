# Include standard modules
from typing import Dict, Set

# Include 3rd-party modules

# Include DPL modules
from dpl.auth import User
from dpl.auth.token_manager import TokenManager


class AuthManager(object):
    """
    AuthManager is a class that controls users and their access to different
    parts of the system
    """
    def __init__(self, insecure: bool = False):
        """
        Constructor. Allows to disable token checking ALTOGETHER.
        USE INSECURE MODE ONLY WHEN YOU KNOW WHAT YOU ARE DOING!
        :param insecure: disable token checking
        """
        self._users = dict()  # type: Dict[str, User]
        self._root_user = None  # type: User
        self._token_manager = TokenManager()
        self._is_insecure = insecure

    @property
    def is_insecure(self) -> bool:
        """
        Indicates is AuthManager in insecure mode. Or, in other words, is token
        checking disabled.
        :return: True if insecure, False otherwise
        """
        return self._is_insecure

    @is_insecure.setter
    def is_insecure(self, new_value: bool):
        """
        Allows to enable secure mode. Only
        :param new_value: new value of is_secure property
        :return: None
        """
        if not isinstance(new_value, bool):
            raise TypeError("The value of 'new_value' parameter must to boolean")

        if new_value:  # if new_value == True:
            raise ValueError("Insecure mode can't be enabled in runtime. Please, edit"
                             "persistent configuration and restart this application.")

        self._is_insecure = new_value

    @property
    def users(self) -> Set[str]:
        """
        Returns a set of registered usernames
        :return: usernames of all registered users
        """
        # FIXME: CC7: Return just plain keys(), as is
        return set(self._users.keys())

    # FIXME: CC4: Maybe return value is needed?
    def create_root_user(self, username: str, password: str):
        """
        Create a root user if there is no users registered
        :param username: a username of root user
        :param password: a password of root user
        :return: None
        """
        if not self._users:
            assert self._root_user is None

            root_user = User(username, password)

            assert username not in self._users
            self._users[username] = root_user
            self._root_user = root_user

        else:
            raise ValueError("Root user creation may be called only once in a system lifecycle")

    def create_user(self, token: str, username: str, password: str):
        """
        Create a user with specified username and password values
        :param token: an access token of a user that is trying to create a new one
        :param username: username of the user to be created
        :param password: password of the user to be created
        :return: None
        """
        # FIXME: check if user with specified token is authorized to create new users
        # There is a temporary solution in the following method:
        self._check_if_authorized_to_manipulate_users(token)

        if username in self._users:
            raise ValueError("User with a specified username is already registered")

        new_user = User(username, password)
        self._users[username] = new_user

    def _check_if_authorized_to_manipulate_users(self, token: str):
        """
        Checks if user with specified token is authorized to create or remove users.
        Otherwise raises an exception.
        :param token: an access token of a user that is trying to create or remove another one
        :return: None
        """
        # FIXME: Temporary solution: only root is authorized to create new users
        requester = self._token_manager.resolve_token_owner(token)

        if requester != self._root_user:
            raise ValueError(
                "Only root user ({0}) is authorized to create new users. "
                "At least for now.".format(self._root_user.username)
            )

    def remove_user(self, token: str, username: str):
        """
        Remove a user from the system
        :param token: an access token of a user that is trying to remove someone
        :param username: a username of the user to be removed
        :return: None
        """
        # FIXME: check if user with specified token is authorized to remove users
        # There is a temporary solution in the following method:
        self._check_if_authorized_to_manipulate_users(token)

        if username == self._root_user.username:
            raise ValueError("Root user can't be removed. You need to reset system settings to do that")

        self._check_user_registered(username)

        user = self._users.pop(username)

        # Remove all tokens for specified user
        self._token_manager.remove_all_tokens(user)

    def change_password(self, username: str, old_password: str, new_password: str):
        """
        Change a password of specific user
        :param username: a username of user whose password must be changed
        :param old_password: an old password of this user
        :param new_password: a new password of this user
        :return: None
        """
        self._check_user_registered(username)

        user = self._users.get(username)

        user.update_password(old_password, new_password)

        # Remove all tokens for specified user
        self._token_manager.remove_all_tokens(user)

    # FIXME: Specify a type of exception
    def _check_user_registered(self, username):
        """
        Checks if the user is registered in the system. Otherwise raises an exception
        :param username: username of user to be checked
        :return: None
        """
        if username not in self._users:
            raise ValueError("There is no users registered with username {0}".format(username))

    def auth_user(self, username: str, password: str) -> str:
        """
        Authenticate the user and receive an access token for future usages
        :param username: username of user to be authenticated
        :param password: password of user to be authenticated
        :return: an access token
        """
        self._check_user_registered(username)

        user = self._users.get(username)

        authenticated = user.verify_password(password)

        if not authenticated:
            raise ValueError("Specified username-password pair is invalid")

        token = self._token_manager.generate_token(user)

        return token

    def is_token_grants(self, token: str, requested_action: object) -> bool:
        """
        Check if specified token grants to perform the requested action
        :param token: an access token
        :param requested_action: an info about the requested action
        :return: true if permission is granted, false otherwise
        """
        # TODO: Implement permission checking
        if self._is_insecure:
            return True  # WARNING: all token values are accepted in insecure mode

        return self._token_manager.is_token_present(token)
