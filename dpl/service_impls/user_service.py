import uuid

from dpl.model.domain_id import TDomainId
from dpl.model.user import User
from dpl.dtos.user_dto import UserDto
from dpl.dtos.dto_builder import build_dto
from dpl.services.abs_user_service import AbsUserService, \
    ServiceEntityResolutionError, AuthInvalidUserPasswordCombinationError

from dpl.repos.abs_user_repository import AbsUserRepository
from .base_observable_service import BaseObservableService, ServiceEventType


class UserService(
    BaseObservableService[User, UserDto],
    AbsUserService
):
    """
    This is an implementation of a UserService - a class
    that manages all Users in the system
    """
    def __init__(self, user_repo: AbsUserRepository):
        """
        Constructor. Receives a repository of Users to be
        managed

        :param user_repo: an instance of AbsUserRepository
        """
        super().__init__()
        self._user_repo = user_repo

    def view_all(self):  # -> Collection[UserDto]:
        """
        Fetch a full list of DTOs of all stored objects

        :return: a collection of DTOs
        """
        return [
            build_dto(user)
            for user in self._user_repo.load_all()
        ]

    def view(self, domain_id: TDomainId) -> UserDto:
        """
        Fetch a DTO of stored object by the ID specified

        :param domain_id: id of object to be fetched
        :return: a DTO of stored object
        :raises ServiceResolutionError: if the entity with
                the specified ID can't be found
        """
        resolved = self._resolve_entity(self._user_repo, domain_id)
        return build_dto(resolved)

    def remove(self, domain_id: TDomainId) -> None:
        """
        REMOVES an Entity with the specified ID altogether
        from the system

        :param domain_id: an identifier of Entity to be deleted
        :return: None
        :raises ServiceResolutionError: if the entity with
                the specified ID can't be found
        :raises ServiceEntityLinkError: if the specified can't
                be removed because some other entity is linked
                (uses or refers) to it
        """
        self._user_repo.delete(domain_id)
        self._notify(
            object_id=domain_id,
            event_type=ServiceEventType.deleted,
            object_dto=None
        )

    def view_by_username(self, username: str) -> UserDto:
        """
        Allows to fetch a User (UserDto, to be exact) by
        User's username

        :param username: username of the User to be fetched
        :return: an instance of User DTO
        :raises ServiceEntityResolutionError: if the User
                with the specified username was not found
        """
        resolved = self._user_repo.find_by_username(username)
        self._check_resolved(resolved)

        return build_dto(resolved)

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
        user = User(
            domain_id=uuid.uuid4().hex,
            username=username,
            password=password
        )

        self._user_repo.add(user)

        self._notify(
            object_id=user.domain_id,
            event_type=ServiceEventType.added,
            object_dto=build_dto(user)
        )

        return user.domain_id

    def verify_password(self, username: TDomainId, password: str) -> bool:
        """
        Allows to check an username-password combination

        :param username: a username of the User
        :param password: a password for the User
        :return: True if User with the specified username exists
                 and have the specified password. False if either
                 User with the specified username isn't existing
                 or if the password is incorrect
        """
        resolved = self._user_repo.find_by_username(username)

        return (resolved is not None) and (resolved.verify_password(password))

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
        resolved = self._user_repo.find_by_username(username)

        if resolved is None:
            raise AuthInvalidUserPasswordCombinationError()

        password_ok = resolved.verify_password(password)

        if not password_ok:
            raise AuthInvalidUserPasswordCombinationError()

        return build_dto(resolved)

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
        user = self._resolve_entity(repository=self._user_repo, domain_id=of_user)
        user.username = new_username

        self._notify(
            object_id=of_user,
            event_type=ServiceEventType.modified,
            object_dto=build_dto(user)
        )

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
        user = self._resolve_entity(repository=self._user_repo, domain_id=of_user)
        user.update_password(old_password, new_password)
