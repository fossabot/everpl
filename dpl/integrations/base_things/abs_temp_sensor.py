# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import HasTemperature


class AbsTemperatureSensor(HasTemperature):
    """
    Temperature Sensor represents simple thermometers, temperature sensors
    which displays the current temperature of controlled object: in-room
    air temperature, outside temperature, temperature of a human body, etc.

    If your device implements some features in addition to measuring of
    temperature - please, consider some other base types for your device.
    """

    _type = "temp_sensor"
