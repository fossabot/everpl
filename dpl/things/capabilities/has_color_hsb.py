"""
This module contains definition of Has Color HSB capability
"""

from .has_brightness import HasBrightness


class HasColorHSB(HasBrightness):
    """
    Has Color HSB devices are devices that have a "color" property. The current
    color is specified using three components: hue, saturation and brightness.
    Each component has its own property with a corresponding name.

    Actuator Has Color devices are able to change their color with a set_color
    command. Usually Color HSB profile is implemented by RGB Light Bulbs.
    """
    _capability_name = 'has_color_hsb'
    _commands = ('set_color', ) + HasBrightness._commands

    @property
    def color_hue(self) -> float:
        """
        Returns the "hue" color component in floating-point values
        from 0.0 to 360.0 including

        :return: the "hue" color component
        """
        raise NotImplementedError()

    @property
    def color_saturation(self) -> float:
        """
        Returns the "saturation" color component in floating-point values
        from 0.0 to 100.0 including

        :return: the "saturation" color component
        """
        raise NotImplementedError()
