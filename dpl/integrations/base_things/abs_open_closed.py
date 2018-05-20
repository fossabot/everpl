# Include standard modules

# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities.open_closed import OpenClosed
from .abs_togglable_actuator import AbsTogglableActuator


class AbsOpenClosed(AbsTogglableActuator, OpenClosed):
    """
    Slider is an abstraction of real-life object, that can be in one of two
    stable states: 'opened' and 'closed' and also can be two transition states:
    'opening' and 'closing'
    """

    @property
    def is_active(self):
        """
        Indicates if the object is in active state

        :return: True if state == 'opened', false otherwise
        """
        return (self.state == self.States.opened
                or self.state == self.States.opening)

    def activate(self) -> None:
        """
        Switches an object to the active ('opened') state

        :return: None
        """
        return self.open()

    def deactivate(self) -> None:
        """
        Switches an object to the inactive ('closed') state

        :return: None
        """
        return self.close()

    def open(self) -> None:
        """
        Switches an object to the 'opening' and then 'opened' state if its
        current state is 'undefined', 'closed' or 'closing'. Command must be
        ignored otherwise.

        :return: None
        """
        raise NotImplementedError()

    def close(self) -> None:
        """
        Switches an object to the 'closing' and then 'closed' state if its
        current state is 'undefined', 'opened' or 'opening'. Command must be
        ignored otherwise.

        :return: None
        """
        raise NotImplementedError()
