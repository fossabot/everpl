"""
This module contains a definition of AuthService interface.

Comparing to the other services, it has a different signature,
is not a child of AbsEntityService and was mainly created as
a facade for two other services - SessionService and UserService
"""

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

    def check_permission(self, access_token: str, to_perform: str) -> None:
        """
        WARNING: check_permission signature is a subject to change!
        Don't use it for now

        FIXME: Define signature

        :param access_token: ???????????
        :param to_perform: ????????????
        :return: ?????????????
        :raises: ????????????
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
