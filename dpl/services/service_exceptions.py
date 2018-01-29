class ServiceValidationError(Exception):
    """
    Exception to be raised on any Service validation errors
    like object resolution failure, invalid arguments, invalid
    combination of arguments and so on
    """
    pass


class ServiceEntityResolutionError(ServiceValidationError):
    """
    Exception to be raised on object resolution failures
    (like object with the specified identifier was deleted
    or not existing at all)
    """
    pass

