# Include standard modules
from enum import Enum
from typing import Tuple

# Include 3rd-party modules
# Include DPL modules
from dpl.things import Actuator


class Switch(Actuator):
    """
    Switch is an abstraction of objects with two only available states: 'on' and 'off'.
    Like simple light bulb, power socket, relay or fan with uncontrollable speed.
    """
    class States(Enum):
        on = True
        off = False
        unknown = None

    @property
    def commands(self) -> Tuple[str, ...]:
        """
        Returns a list of available commands. Must be overridden in derivative classes.
        :return: a tuple of command names (strings)
        """
        return super().commands + ('on', 'off')

    @property
    def is_active(self):
        """
        Indicates if the object is in active state
        :return: True if state == 'on', false otherwise
        """
        return self.state == self.States.on

    def activate(self) -> None:
        """
        Switches an object to the active ('on') state
        :return: None
        """
        return self.on()

    def deactivate(self) -> None:
        """
        Switches an object to the inactive ('off') state
        :return: None
        """
        return self.off()

    def on(self) -> None:
        """
        Switches an object to the 'on' state
        :return: None
        """
        raise NotImplementedError

    def off(self) -> None:
        """
        Switches an object to the 'off' state
        :return: None
        """
        raise NotImplementedError
