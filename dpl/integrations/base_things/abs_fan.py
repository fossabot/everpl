# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from .abs_on_off import AbsOnOff


class AbsFan(AbsOnOff):
    """
    AbsFan is an abstraction of all externally controllable Fans - the most
    primitive type of the climatic devices.

    Fans can be either in "on" or "off" states while fan speed control is not
    supported. Additional functionality like enabling and disabling heaters is
    not supported too.
    """
    _type = "fan"
