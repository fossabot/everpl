"""
This module contains definition of Has Volume capability
"""

from dpl.utils.color_rgb import ColorRGB


class HasVolume(object):
    """
    Has Value devices are devices that have the "volume" property - the
    measure of loudness, i.e. of how loud its sound is. Volume is an integer
    value in the range from 0 (zero) to 100 including.

    Actuator Has Volume devices are able to change their volume with a
    set_volume command.
    """
    _capability_name = 'has_volume'
    _commands = ('set_volume', )

    @property
    def volume(self) -> ColorRGB:
        """
        Returns the current color for this Thing in RGB format

        :return: the current color for this Thing in RGB format
        """
        raise NotImplementedError()
