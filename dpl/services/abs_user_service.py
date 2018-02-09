from dpl.model.domain_id import TDomainId
from dpl.dtos.user_dto import UserDto
from .abs_entity_service import AbsEntityService


class AbsUserService(AbsEntityService[UserDto]):
    """
    A base class for all UserService implementations
    """
    def create_user(self, username: str, password: str) -> TDomainId:
        """
        Creates a new user in the system with the specified
        username and password. Password value must NOT to be
        saved as a plain text

        :param username: username, login name of the User
               to be created
        :param password: password of the User to be created
        :return: an unique identifier of the User
        """
        raise NotImplementedError()

    def change_username(self, of_user: TDomainId, new_username: str) -> None:
        """
        Allows to change the username for the specified User

        :param of_user: an identifier of the User (NOT username
               but domain identifier) to be altered
        :param new_username: new username to be set for the User
        :return: None
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
        :return:
        # FIXME: Document possible exceptions
        """
        raise NotImplementedError()

