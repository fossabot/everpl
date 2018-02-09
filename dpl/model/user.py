# Include standard modules


# Include 3rd-party modules
import passlib
from passlib.ifc import PasswordHash
from passlib.hash import pbkdf2_sha256

# Include DPL modules
from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity


# Specify used hasher
Hasher = pbkdf2_sha256  # type: PasswordHash

# Patch old versions of passlib
if passlib.__version__ < '1.7':
    Hasher.hash = Hasher.encrypt


class User(BaseEntity):
    """
    User is a class that stores all information about one of the users
    of the system. Including a list of connected client devices.
    """
    def __init__(self, domain_id: TDomainId, username: str, password: str):
        """
        Create a user of the system

        :param domain_id: a unique identifier of this User
        :param username: username to be used
        :param password: password to be used. NOT SAVED, just hashed
        """
        super().__init__(domain_id)

        self._username = None  # type: str

        self.username = username  # set actual value and ensure its validity
        self._pwd_hash = Hasher.hash(password)  # type: str

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

