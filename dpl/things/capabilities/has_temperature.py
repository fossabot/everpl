"""
This module contains definition of Has Temperature capability
"""


class HasTemperature(object):
    """
    Has Temperature devices are devices that have the "temperature" property.
    The value of "temperature_c" property is expressed in degrees of Celsius,
    Fahrenheits are not supported for now.

    It's supposed that the value of "temperature" property can'be changed by
    user and represents the current, real temperature of controlled object.
    For other purposes, please refer to Capability and Thing types which
    provide a "target_temperature" property.
    """
    _capability_name = 'has_temperature'

    @property
    def temperature_c(self) -> float:
        """
        Returns the current Thing temperature in degrees of Celsius

        :return: the current Thing temperature in degrees of Celsius
        """
        raise NotImplementedError()
