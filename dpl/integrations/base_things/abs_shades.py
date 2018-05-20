# Include standard modules

# Include 3rd-party modules
# Include DPL modules
from .abs_open_closed import AbsOpenClosed


class AbsShades(AbsOpenClosed):
    """
    AbsShades is an abstraction of all shades - objects which cover the
    window and reduce the amount of light passed through it. Also named as
    sunblinds, shutters, louvers and so on.

    Their state can take either "opened" or "closed" values, where "opened"
    is equal to "active" and "closed" equal to "not active". Two transitional
    states are also possible: "opening" and "closing".

    This base class doesn't implement the Has Position capability.
    """
    _type = "shades"
