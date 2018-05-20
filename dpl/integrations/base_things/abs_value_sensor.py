# Include standard modules
from typing import TypeVar

# Include 3rd-party modules
# Include DPL modules
from dpl.things.thing import Thing
from dpl.things.capabilities import HasValue

T = TypeVar('T')


class AbsValueSensor(Thing, HasValue[T]):
    """
    A generic type of sensors which represent their results of measurements
    in numbers of an unspecified unit. Must to be used rarely, only if
    there is no more specific device type declared.

    Measured values must to be displayed to user in the same manner:
    "current value is %d", where "%d" is an placeholder for the measured value.
    """

    _type = "value_sensor"
