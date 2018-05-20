# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from .abs_binary_sensor import AbsBinarySensor


class AbsSwitch(AbsBinarySensor):
    """
    Another kind of a Binary Sensor. Is a base type for devices which can
    preserve their state without the help of a user (i.e. user doesn't need
    to keep the switch pressed).

    Physically, it can be a simple light switch, toggle switch,
    reed switch and on and on.

    As any other Binary Sensor, the "value" field value can be equal to either
    1 or 0, where 1 is mapped to "active" and 0 is mapped to "not active".
    """
    _type = "switch"
