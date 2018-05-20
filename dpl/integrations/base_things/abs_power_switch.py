# Include standard modules

# Include 3rd-party modules
# Include DPL modules
from .abs_on_off import AbsOnOff


class AbsPowerSwitch(AbsOnOff):
    """
    AbsOnOff is an abstraction of all power switches in the system.

    The only functionality of such devices is to turn connected load on
    and off. Such power switches include smart power outlet, circuit breakers,
    switches that are not Light switches and other similar devices.
    """
    _type = "power_switch"
