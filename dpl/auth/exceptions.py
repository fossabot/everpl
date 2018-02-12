"""
This module contains a list of all possible exceptions
to be raised by AuthService
"""

from dpl.services.service_exceptions import ServiceValidationError


class AuthInsufficientPrivilegesError(ServiceValidationError):
    """
    Exception to be raised if the current User or
    client application doesn't have enough privileges to
    preform the requested action
    """
    pass


class AuthInvalidUserPasswordCombinationError(ServiceValidationError):
    """
    Exception to be raised on User login if either User
    with the specified username is not existing in the
    system or if the specified password is invalid
    """
    pass


class AuthInvalidTokenError(ServiceValidationError):
    """
    Exception to be raised if either the specified token
    was revoked or was not existing at all
    """
    pass
