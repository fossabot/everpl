from typing import Iterable, Mapping

from dpl.utils.empty_mapping import EMPTY_MAPPING

from .has_state import HasState


class UnsupportedCommandError(ValueError):
    """
    An exceptions to be raised if the specified command
    is not supported by this instance of Thing
    """
    pass


class UnacceptableCommandArgumentsError(Exception):
    """
    An exception to be raised if at least one of the specified
    command arguments has an unacceptable type or if there is
    an incorrect set of arguments passed (i.e. if one of the
    mandatory arguments is missing or if one of the specified
    arguments is extra and isn't related to the specified command)
    """
    pass


class Actuator(HasState):
    """
    Actuator capability is usually mapped to Actuators.
    Devices with this capability are capable to act, i.e.
    perform some actions in the real world like playing
    music and changing tracks, turning power on and off,
    turning light on and off and so on.
    """
    @property
    def commands(self) -> Iterable[str]:
        """
        Returns a list of command (command names) that
        can be executed by this Thing.

        Availability of the following commands is mandatory:

        - activate;
        - deactivate;
        - toggle.

        For details about such commands see the definition
        of the corresponding methods

        :return: a list of commands that can be executed by
                 this Thing
        """
        raise NotImplementedError()

    def execute(self, command: str, args: Mapping = EMPTY_MAPPING) -> None:
        """
        Accepts the specified command on execution

        :param command: a name of command to be executed
               (see 'commands' property for a list of
                available commands)
        :param args: a mapping with keyword arguments to be
               passed on command execution
        :return: None
        """
        raise NotImplementedError()

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
        Switched the Thing from a current state to an
        opposite one (deactivates if active, activates if
        inactive)

        :return: None
        """
        raise NotImplementedError()
