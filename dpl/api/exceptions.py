"""
Exceptions is a package that contains all of the exceptions, that can be raised by
ApiGateway and other classes in dpl.api module.
"""


# Exceptions of ApiGateway:

class PermissionDeniedForTokenError(PermissionError):
    pass


class ResourceNotFoundError(ValueError):
    pass


class ThingNotFoundError(ResourceNotFoundError):
    pass


class PlacementNotFoundError(ResourceNotFoundError):
    pass


class CommandFailedError(ValueError):
    pass


class CommandNotOnActuatorError(CommandFailedError):
    pass

