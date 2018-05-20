# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import HasColorHSB
from .abs_ct_light import AbsColorTemperatureLight


class AbsColorLight(AbsColorTemperatureLight, HasColorHSB):
    """
    AbsColorTemperatureLight is an abstraction of all lighting devices with
    controllable color temperature
    """
    _type = "color_light"

    def set_color(self, hue: float, saturation: float) -> None:
        """
        Sets the new value of color for this Thing using HSB format.
        The brightness is expected to be left unchanged

        :param hue: a new value for color hue to be set;
               floating point values from 0.0 including
               to 360.0 not including
        :param saturation: a new value for color saturation to be set;
               floating point values from 0.0 to 100.0 including
        :return: None
        """
        raise NotImplementedError()
