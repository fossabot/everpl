# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from .abs_on_off import AbsOnOff


class AbsLight(AbsOnOff):
    """
    AbsOnOff is an abstraction of lighting devices like light bulbs,
    LED strips and so on.
    """
    _type = "light"
