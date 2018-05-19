"""
This module contains definition of Has Color Temperature capability
"""


class HasColorTemperature(object):
    """
    Color Temperature devices are devices that have the "color temperature"
    property. The color temperature is expressed in Kelvins and can take integer
    values from 1000 to 10000 including. The color temperature of light source
    or other Actuator can be set with ``set_color_temp`` command.

    If the Thing doesn't support specified color temperature value
    (i.e. it's too low or too high for this Thing), then the color temperature
    will be set to the nearest supported value.
    """
    _capability_name = 'has_color_temp'
    _commands = ('set_color_temp',)

    @property
    def color_temp(self) -> int:
        """
        Returns the current color temperature of a Thing in Kelvins

        :return: the current color temperature in Kelvins
        """
        raise NotImplementedError()
