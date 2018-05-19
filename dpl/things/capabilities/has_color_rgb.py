"""
This module contains definition of Has Color RGB capability
"""

from dpl.utils.color_rgb import ColorRGB


class HasColorRGB(object):
    """
    Has Color HSB devices are devices that have a "color" property. The current
    color is specified using three components: reg, green and blue components.
    Each component has its own property with a corresponding name.

    Actuator Has Color devices are able to change their color with a set_color
    command. Usually Color RGB profile is implemented by color sensors.
    """
    _capability_name = 'has_color_rgb'
    _commands = ('set_color', )

    @property
    def color_rgb(self) -> ColorRGB:
        """
        Returns the current color for this Thing in RGB format

        :return: the current color for this Thing in RGB format
        """
        raise NotImplementedError()

    @property
    def saturation(self) -> float:
        """
        Returns the "saturation" color component in floating-point values
        from 0.0 to 100.0 including

        :return: the "saturation" color component
        """
        raise NotImplementedError()
