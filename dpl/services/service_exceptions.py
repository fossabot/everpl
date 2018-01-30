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


class ServiceEntityLinkError(ServiceValidationError):
    """
    Exception to be raised if the object is currently used
    or linked by an another object and thus can't be deleted
    """
    pass


class ServiceTypeError(ServiceValidationError):
    """
    Exception to be raised if the specified object can't
    be used for the specified context (i.e. that the specified
    Thing can't execute commands)
    """
    pass

