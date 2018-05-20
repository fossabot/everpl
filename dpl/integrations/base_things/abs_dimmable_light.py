# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import HasBrightness
from .abs_light import AbsLight


class AbsDimmableLight(AbsLight, HasBrightness):
    """
    AbsOnOff is an abstraction of all dimmable lighting devices, i.e. for all
    lighting devices which can change their brightness.
    """
    _type = "dimmable_light"

    def set_brightness(self, brightness: float) -> None:
        """
        Sets the new value of brightness for this Thing

        :param brightness: a new value to be set; floats from 0.0 to 100.0
        :return: None
        """
        raise NotImplementedError()
