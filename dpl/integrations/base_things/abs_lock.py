# Include standard modules

# Include 3rd-party modules
# Include DPL modules
from .abs_open_closed import AbsOpenClosed


class AbsLock(AbsOpenClosed):
    """
    AbsLock is an abstraction of all externally controllable Locks. Allows
    to lock AND unlock the controlled door, gate or another object.

    The "state" field can take either one of the end state values ("opened" or
    "closed") or one of the transitional state values ("opening", "closing").
    """
    _type = "lock"
