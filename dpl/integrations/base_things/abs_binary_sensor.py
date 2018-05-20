# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import IsActive
from .abs_value_sensor import AbsValueSensor


class AbsBinarySensor(AbsValueSensor[bool], IsActive):
    """
    The most primitive (but not necessary the base) type of Sensors in the
    system. Can have only one of two integer values: 1 and 0. Where 1 is
    mapped to the "active" state and 0 is mapped to "not active".

    Usually is inherited by more specific implementations of a Binary Sensor,
    including buttons, leakage sensors, reed switches (detects an opening
    of a door or window), motion sensors and so on.
    """
    _type = "binary_sensor"

    @property
    def is_active(self) -> bool:
        """
        Returns if this object is currently in one of the
        'active' states (like 'on' for lighting, 'open'
        for a door and 'playing' for player)

        :return: True if the measured value for the sensor is not zero
                 (i.e. is 1) or is True
        """
        return bool(self.value)
