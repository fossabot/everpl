# Include standard modules
from enum import Enum
from typing import Tuple

# Include 3rd-party modules
# Include DPL modules
from dpl.connections import Connection
from dpl.things import Actuator


class Slider(Actuator):
    """
    Slider is an abstraction of real-life object, that can be in one of two
    stable states: 'opened' and 'closed' and also can be two transition states:
    'opening' and 'closing'
    """
    class States(Enum):
        closed  = 0b00
        opening = 0b01
        closing = 0b10
        opened  = 0b11
        unknown = None

    def commands(self) -> Tuple[str, ...]:
        """
        Returns a list of available commands. Must be overridden in derivative classes.
        :return: a tuple of command names (strings)
        """
        return super().commands + ('open', 'close')

    @property
    def is_active(self):
        """
        Indicates if the object is in active state
        :return: True if state == 'on', false otherwise
        """
        return self.state == self.States.opened

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
        Switches an object to the 'opening' and then 'opened' state if its current state
        is 'undefined', 'closed' or 'closing'. Command must be ignored otherwise.
        :return: None
        """
        raise NotImplementedError

    def close(self) -> None:
        """
        Switches an object to the 'closing' and then 'closed' state if its current state
        is 'undefined', 'opened' or 'opening'. Command must be ignored otherwise.
        :return: None
        """
        raise NotImplementedError
