"""
This module contains a definition of an AbsTogglableActuator base class
"""

from dpl.things.capabilities import IsActive
from .abs_actuator import AbsActuator


class AbsTogglableActuator(AbsActuator, IsActive):
    """
    AbsTogglableActuator is a base class for Actuators which implement
    IsActive interface in general and "toggle" method in particular
    """

    def activate(self) -> None:
        """
        Switches the Thing to one of the 'active' states

        :return: None
        """
        raise NotImplementedError()

    def deactivate(self) -> None:
        """
        Switches the Thing to one of the 'inactive' states

        :return: None
        """
        raise NotImplementedError()

    def toggle(self) -> None:
        """
        Switches an object from the current state to the opposite one

        :return: None
        """
        if self.is_active:
            return self.deactivate()
        else:
            return self.activate()
