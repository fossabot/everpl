# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import HasState, OpenClosed
from .abs_switch import AbsSwitch


class AbsContactSensor(AbsSwitch, OpenClosed, HasState):
    """
    The special subtype of a Switch. Adds a new field to the list: a
    "has_state" field which can take either "opened" or "closed" value,
    where "opened" is equal to 1 and "closed" is equal to 0.
    """
    _type = "contact_sensor"

    @property
    def state(self) -> OpenClosed.States:
        """
        Return a current state of the Thing

        :return: an instance of self.State
        """
        if self.value is None:
            return self.States.unknown
        elif self.value:
            return self.States.opened
        else:
            return self.States.closed
