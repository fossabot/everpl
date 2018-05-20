# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from .abs_binary_sensor import AbsBinarySensor


class AbsButton(AbsBinarySensor):
    """
    An abstraction of all the Buttons connected to the system.

    Its value is set to 1 while the button is pressed and sets to 0 just after
    the button was released. There is no long press detection, double press
    detection and so on. Just "pressed" (1) and released (0).

    All the other functionality is the same as in Binary Sensor.
    """
    _type = "button"
