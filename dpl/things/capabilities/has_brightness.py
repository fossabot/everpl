"""
This module contains definition of Has Brightness capability
"""


class HasBrightness(object):
    """
    Has Brightness devices are devices that have the ``brightness`` property.

    Actuator Has Brightness devices are able to change their brightness with a
    ``set_brightness`` command. Usually normal people call Actuator Has
    Brightness devices "dimmable" devices.
    """
    _capability_name = 'has_brightness'
    _commands = ('set_brightness',)

    @property
    def brightness(self) -> float:
        """
        Returns the current brightness of a Thing in floating-point values from
        0.0 to 100.0

        :return: the current brightness of a Thing
        """
        raise NotImplementedError()
