# Include standard modules

# Include 3rd-party modules
# Include DPL modules
from .abs_open_closed import AbsOpenClosed


class AbsDoorActuator(AbsOpenClosed):
    """
    AbsDoorActuator is an abstraction of all door actuators - mechanisms which
    are able to open and close the physical door, gate or other similar object.

    The "state" field can take either one of the end state values ("opened" or
    "closed") or one of the transitional state values ("opening", "closing").
    """
    _type = "door_actuator"
