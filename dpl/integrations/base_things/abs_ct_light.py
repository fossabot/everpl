# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import HasColorTemperature
from .abs_dimmable_light import AbsDimmableLight


class AbsColorTemperatureLight(AbsDimmableLight, HasColorTemperature):
    """
    AbsColorTemperatureLight is an abstraction of all lighting devices with
    controllable color temperature
    """
    _type = "ct_light"

    def set_color_temp(self, color_temp: int) -> None:
        """
        Sets the new value of color temperature for this Thing

        :param color_temp: a new value to be set; integers from 1000 to 100000
        :return: None
        """
        raise NotImplementedError()
