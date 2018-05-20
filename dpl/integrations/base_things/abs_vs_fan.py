# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import FanSpeed
from .abs_fan import AbsFan


class AbsVariableSpeedFan(AbsFan, FanSpeed):
    """
    AbsVariableSpeedFan is an abstraction of all Fans with externally
    controllable rotation speed. Adds an additional "fan_speed" property
    and a corresponding "set_fan_speed" command to the base Fan class
    """
    _type = "vs_fan"

    def set_fan_speed(self, fan_speed: float) -> None:
        """
        Sets the new fan rotation speed for a Thing.

        :param fan_speed: the new value to be set in units from 0.0 to 100.0
        :return: None
        """
        raise NotImplementedError()
