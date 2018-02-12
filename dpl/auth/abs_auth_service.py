"""
This module contains a definition of AuthService interface.

Comparing to the other services, it has a different signature,
is not a child of AbsEntityService and was mainly created as
a facade for two other services - SessionService and UserService
"""

from dpl.dtos.session_dto import SessionDto


from .exceptions import (
    AuthInvalidUserPasswordCombinationError,
    AuthInsufficientPrivilegesError,
    AuthInvalidTokenError
)


class AbsAuthService(object):
    """
    AuthService is responsible for managing user Authentication
    and Authorization, issuing access tokens to the client
    devices and applications, changing user passwords and
    performing of token revocation.

    A base class for all AuthService implementations
    """
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
        raise NotImplementedError()

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
        raise NotImplementedError()

    def check_permission(
            self, access_token: str,
            in_domain: str, to_execute: str,
            *args, **kwargs
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
        raise NotImplementedError()

    def view_sessions(self, access_token: str):  # -> Collection[SessionDto]
        """
        Allows to view all Sessions opened for the current User

        :param access_token: an access token used for User
               identification and authorization
        :return: a collection of DTOs of Sessions that was opened
                 for the specified User
        """
        raise NotImplementedError()

    def view_current_session(self, access_token: str) -> SessionDto:
        """
        Allows to view information about the current Session
        which is associated with the specified access token

        :param access_token: an access token which is associated
               with the current Session
        :return: information about a current opened Session in
                 a form of a DTO
        """
        raise NotImplementedError()

    def close_session(self, access_token: str) -> None:
        """
        Closes current session (i.e. performs a logout).

        Returns silently (i.e. without exceptions) if the specified
        access token was revoked already or not was not existing
        at all.

        :param access_token: an access token of the current Session
        :return: None
        """
        raise NotImplementedError()

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
        raise NotImplementedError()
