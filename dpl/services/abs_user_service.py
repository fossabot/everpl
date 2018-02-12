from dpl.model.domain_id import TDomainId
from dpl.dtos.user_dto import UserDto
from dpl.auth.exceptions import AuthInvalidUserPasswordCombinationError
from .service_exceptions import ServiceEntityResolutionError, ServiceValidationError
from .abs_entity_service import AbsEntityService


class AbsUserService(AbsEntityService[UserDto]):
    """
    A base class for all UserService implementations
    """
    def view_by_username(self, username: str) -> UserDto:
        """
        Allows to fetch a User (UserDto, to be exact) by
        User's username

        :param username: username of the User to be fetched
        :return: an instance of User DTO
        :raises ServiceEntityResolutionError: if the User
                with the specified username was not found
        """
        raise NotImplementedError()

    def create_user(self, username: str, password: str) -> TDomainId:
        """
        Creates a new user in the system with the specified
        username and password. Password value must NOT to be
        saved as a plain text

        :param username: username, login name of the User
               to be created
        :param password: password of the User to be created
        :return: an unique identifier of the User
        # FIXME: Document exceptions
        """
        raise NotImplementedError()

    def verify_password(self, username: str, password: str) -> bool:
        """
        Allows to check an username-password combination

        :param username: a username of the User
        :param password: a password for the User
        :return: True if User with the specified username exists
                 and have the specified password. False if either
                 User with the specified username isn't existing
                 or if the password is incorrect
        """
        raise NotImplementedError()

    def authenticate(self, username: str, password: str) -> UserDto:
        """
        Authenticate the User by the specified username-password
        combination.

        :param username: username of the User to be authenticated
        :param password: password of the User to be authenticated
        :return: an instance of User (User DTO, to be exact)
                 which has the specified username-password combination
        :raises AuthInvalidUserPasswordCombinationError:
                if the specified username-password combination is invalid
        """
        raise NotImplementedError()

    def change_username(self, of_user: TDomainId, new_username: str) -> None:
        """
        Allows to change the username for the specified User

        :param of_user: an identifier of the User (NOT username
               but domain identifier) to be altered
        :param new_username: new username to be set for the User
        :return: None
        :raises ServiceEntityResolutionError: if the User with
                the specified ID was not found
        # FIXME: Document other exceptions
        """
        raise NotImplementedError()

    def change_password(self, of_user: TDomainId, old_password: str, new_password: str) -> None:
        """
        Allows to change a password for a User from old_password
        to the new_password

        :param of_user: an identifier of the User (NOT username
               but domain identifier) to be altered
        :param old_password: old password for this user
        :param new_password: new password to be set for this user
        :return: None
        :raises ServiceEntityResolutionError: if the User with
                the specified ID was not found
        # FIXME: Document other exceptions
        """
        raise NotImplementedError()

