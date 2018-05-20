# Include standard modules
from enum import Enum

# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import OnOff, IsActive
from .abs_actuator import AbsActuator


class AbsOnOff(AbsActuator, OnOff, IsActive):
    """
    AbsOnOff is an abstraction of objects with two only available states: 'on'
    and 'off'. Like simple light bulb, power socket, relay or fan with
    uncontrollable speed.
    """
    class States(Enum):
        on = 1
        off = 0
        unknown = -1

    @property
    def is_active(self) -> bool:
        """
        Returns if this object is currently in the 'active' ('on') state

        :return: True if object is in 'active' states ('on') state,
                 False otherwise
        """
        return self.state == self.States.on

    def on(self) -> None:
        """
        Switches an object to the 'on' state

        :return: None
        """
        raise NotImplementedError()

    def off(self) -> None:
        """
        Switches an object to the 'off' state

        :return: None
        """
        raise NotImplementedError()

    def activate(self) -> None:
        """
        Switches an object to the 'active' ('on') state

        :return: None
        """
        return self.on()

    def deactivate(self) -> None:
        """
        Switches an object to the 'non-active' ('off') state

        :return: None
        """
        return self.off()

    def toggle(self) -> None:
        """
        Switches an object between the opposite ('on' and 'off') states

        :return: None
        """
        if self.is_active:
            self.deactivate()
        else:
            self.activate()
