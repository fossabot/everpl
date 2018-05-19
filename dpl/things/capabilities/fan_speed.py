"""
This module contains definition of Fan Speed capability
"""


class FanSpeed(object):
    """
    Fan Speed devices are devices that have a build-in and externally
    controllable (at least monitored) fan. For example, that can be
    heaters, some HVACs and fans itself (as separate devices).

    The speed of some fans can be changed only by a constant step.
    For such cases (for example, for table fans with only 3 speeds),
    the whole range will be separated on the corresponding number
    of segments. For example, it'll be 0-25, 26-50, 51-75 and 76-100
    for a generic fan with speeds 0 (stopped), 1, 2 and 3 correspondingly.

    """
    _capability_name = 'fan_speed'
    _commands = ('set_fan_speed',)

    @property
    def fan_speed(self) -> float:
        """
        Returns the current fan speed of a Thing in values from 0.0 to 100.0.

        :return: the current fan speed
        """
        raise NotImplementedError()
