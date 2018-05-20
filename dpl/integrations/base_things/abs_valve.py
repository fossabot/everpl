# Include standard modules

# Include 3rd-party modules
# Include DPL modules
from .abs_open_closed import AbsOpenClosed


class AbsValve(AbsOpenClosed):
    """
    AbsShades is an abstraction of all externally controllable valves for gas,
    liquid or other matter which can be either in "opened" or "closed" state.
    Transitional states "opening" and "closing" are also possible.
    """
    _type = "valve"
