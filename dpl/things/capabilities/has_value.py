from typing import TypeVar, Generic, Optional

TValueType = TypeVar['TValueType']


class HasValue(Generic[TValueType]):
    """
    Objects with HasValue capability are usually mapped to
    sensors. They allow to read the current measurements
    like the current temperature, humidity or brightness
    levels.
    """
    _capability_name = 'has_value'

    @property
    def value(self) -> Optional[TValueType]:
        """
        Returns the current (last known for unavailable
        state) value read from the internal sensors. Or
        returns a value that provides a detailed
        information about the current state of a Thing
        (like the current track playing for Player or
        current brightness for a Lamp)

        :return: the current value from internal sensors
                 of Thing or some similar information.
                 Or None if the value is not yet known
        """
        raise NotImplementedError()
