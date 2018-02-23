from typing import Sequence, Mapping
from dpl.utils.empty_mapping import EMPTY_MAPPING

from dpl.dtos.session_dto import SessionDto
from dpl.services.service_exceptions import ServiceEntityResolutionError
from dpl.services.abs_user_service import AbsUserService
from dpl.services.abs_session_service import AbsSessionService

from .abs_auth_service import (
    AbsAuthService,
    AuthInvalidUserPasswordCombinationError,
    AuthInvalidTokenError,
    AuthInsufficientPrivilegesError
)


class AuthService(AbsAuthService):
    """
    An implementation of the AbsAuthService interface
    """
    def __init__(self, user_service: AbsUserService, session_service: AbsSessionService):
        """
        Constructor. Receives instances of UserService and
        SessionService to be used to control User's passwords
        and their Sessions

        :param user_service: an instance of UserService
        :param session_service: an instance of SessionService
        """
        self._user_service = user_service
        self._session_service = session_service

    def request_access(
            self, username: str, password: str, client_info: str,
            client_ip: str
    ) -> str:
        """
        Verifies username-password combination, initializes a
        new Session for a client device or application and,
        if everything was successful, returns a generated access
        token

        :param username: username of the User to login
        :param password: password of the User to login
        :param client_info: information about client device or
               application which requested access on behalf of the
               specified User
        :param client_ip: a network address (IP) of a device from
               which the access was requested
        :return: an access token to be used by client device or
                 application to access to the system
        :raises AuthInvalidUserPasswordCombinationError:
                if the specified username-password combination is
                invalid
        """
        user_dto = self._user_service.authenticate(username, password)

        session_id = self._session_service.create_session(
            user_id=user_dto['domain_id'],
            client_info=client_info,
            client_ip=client_ip
        )

        access_token = self._session_service.get_access_token(session_id)

        return access_token

    def change_password(self, access_token: str, old_password: str, new_password: str) -> None:
        """
        Changes a password of the User from old_password to the
        new_password. access_token parameter is used for User
        identification and authorization.

        WARNING: This method revokes all User's Sessions except
        the current one

        :param access_token: an access token which identifies
               the User and grants an access to change User's
               password
        :param old_password: an old password of the User
        :param new_password: a password to be set
        :return: None
        :raises AuthInvalidTokenError: if the specified access
                token is invalid (i.e. was revoked or not
                existing at all)
        :raises AuthInsufficientPrivilegesError: if the specified
                access token doesn't permit password changing
        :raises AuthInvalidUserPasswordCombinationError:
                if the specified old password value is invalid
        """
        session_dto = self._session_service.view_by_access_token(access_token)
        user_id = session_dto['user_id']

        self._user_service.change_password(
            of_user=user_id,
            old_password=old_password,
            new_password=new_password
        )

        self._session_service.close_all_user_sessions(
            for_user=user_id,
            excluding=access_token
        )

    def check_permission(
            self, access_token: str,
            in_domain: str, to_execute: str,
            args: Sequence = (), kwargs: Mapping = EMPTY_MAPPING
    ) -> None:
        """
        Checks if the the specified access token allows to execute
        the specified command in the specified domain with the
        specified keyword and positional arguments.

        Keyword and positional arguments are optional and may be used
        for some contextual checks like "User requested information
        about its own account" or "User has access to the resource
        with the specified identifier" and so on.

        :param access_token: access token to be checked on a
               sufficiency of permissions
        :param in_domain: some domain in which the command is
               executed like 'users' or 'placements'; is usually
               set to the name of a corresponding Service
        :param to_execute: command or method that was requested to
               be executed
        :param args: optional additional positional arguments to be
               checked
        :param kwargs: optional additional keyword arguments to be
               checked
        :return: None
        :raises AuthInvalidTokenError: if the specified access
                token is invalid (i.e. was revoked or not
                existing at all)
        :raises AuthInsufficientPrivilegesError: if the specified
                access token doesn't permit password changing
        """
        # FIXME: Implement full permission checking
        try:
            session = self.view_current_session(access_token)

        except ServiceEntityResolutionError as e:
            raise AuthInvalidTokenError() from e

    def view_sessions(self, access_token: str):  # -> Collection[SessionDto]
        """
        Allows to view all Sessions opened for the current User

        :param access_token: an access token used for User
               identification and authorization
        :return: a collection of DTOs of Sessions that was opened
                 for the specified User
        """
        current_session = self.view_current_session(access_token)
        user_id = current_session['user_id']

        return self._session_service.view_by_user(user_id)

    def view_current_session(self, access_token: str) -> SessionDto:
        """
        Allows to view information about the current Session
        which is associated with the specified access token

        :param access_token: an access token which is associated
               with the current Session
        :return: information about a current opened Session in
                 a form of a DTO
        """
        return self._session_service.view_by_access_token(access_token)

    def close_session(self, access_token: str) -> None:
        """
        Closes current session (i.e. performs a logout).

        Returns silently (i.e. without exceptions) if the specified
        access token was revoked already or not was not existing
        at all.

        :param access_token: an access token of the current Session
        :return: None
        """
        try:
            session_dto = self._session_service.view_by_access_token(access_token)
            session_id = session_dto['domain_id']
            self._session_service.remove(domain_id=session_id)

        except ServiceEntityResolutionError:
            pass

    def close_all_other_sessions(self, access_token: str) -> None:
        """
        Closes (i.e. deletes) all sessions for the User except
        the current one (except the Session with the specified
        access token)

        :param access_token: an access token of the current Session
        :return: None
        :raises AuthInvalidTokenError: if the specified access
                token is invalid (i.e. was revoked or not
                existing at all)
        :raises AuthInsufficientPrivilegesError: if the specified
                access token doesn't permit session revocation
        """
        try:
            session_dto = self._session_service.view_by_access_token(access_token)

        except ServiceEntityResolutionError as e:
            raise AuthInvalidTokenError from e

        session_id = session_dto['domain_id']
        user_id = session_dto['user_id']

        self._session_service.close_all_user_sessions(
            for_user=user_id,
            excluding=session_id
        )
