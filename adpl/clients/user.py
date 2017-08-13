# Include standard modules


# Include 3rd-party modules
from passlib.ifc import PasswordHash
from passlib.hash import pbkdf2_sha256 as Hasher

# Include DPL modules


class User(object):
    """
    User is a class that stores all information about one of the users
    of the system. Including a list of connected client devices.
    """
    def __init__(self, username: str, password: str):
        """
        Create a user of the system
        :param username: username to be used
        :param password: password to be used. NOT SAVED, just hashed
        """
        self._username = None  # type: str

        self.username = username  # set actual value and ensure its validity
        self._pwd_hash = Hasher.hash(password)  # type: PasswordHash

    @property
    def username(self) -> str:
        """
        Returns a username of this user
        :return: username as a string
        """
        return self._username

    @username.setter
    def username(self, value: str):
        """
        Updates the username of the user
        :param value: new username to be set
        :return: None
        """
        if self._is_username_valid(value):
            self._username = value
        else:
            raise ValueError("Invalid username")

    @staticmethod
    def _is_username_valid(username: str) -> bool:
        """
        Checks is the specified username is valid
        :param username: username to be checked
        :return: true if valid, false otherwise
        """
        # Maybe change it:
        return len(username) > 0

    def verify_password(self, password: str) -> bool:
        """
        Checks is the password is correct for this user
        :param password: password to be checked
        :return: true if password is correct and false otherwise
        """
        return Hasher.verify(password, self._pwd_hash)

    def update_password(self, old_password: str, new_password: str):
        """
        Updates current user password, raises an error if old_password is incorrect
        :param old_password: old password
        :param new_password: new password to be set
        :return: None
        """
        if not self.verify_password(old_password):
            raise ValueError("The old password specified is invalid")

        new_hash = Hasher.hash(new_password)
        self._pwd_hash = new_hash

