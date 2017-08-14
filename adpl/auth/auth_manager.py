# Include standard modules
from typing import Dict

# Include 3rd-party modules

# Include DPL modules
from adpl.auth import User
from adpl.auth.token_manager import TokenManager


class AuthManager(object):
    """
    AuthManager is a class that controls users and their access to different
    parts of the system
    """
    def __init__(self):
        self._users = set()  # type: Dict[str, User]
        self._root_user = None  # type: User
        self._token_manager = TokenManager()

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

            assert self._users.get(username, None) is None
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

        if username in self._users:
            raise ValueError("User with a specified username is already registered")

        new_user = User(username, password)
        self._users[username] = new_user

    def remove_user(self, token: str, username: str):
        """
        Remove a user from the system
        :param token: an access token of a user that is trying to remove someone
        :param username: a username of the user to be removed
        :return: None
        """
        # FIXME: check if user with specified token is authorized to remove users

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
