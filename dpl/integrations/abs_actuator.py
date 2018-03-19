# Include standard modules
import time
from typing import Iterable, Mapping

# Include 3rd-party modules
from dpl.utils.empty_mapping import EMPTY_MAPPING

# Include DPL modules
from dpl.things.capabilities.state import State
from dpl.things.capabilities.actuator import (
    Actuator,
    UnsupportedCommandError,
    UnacceptableCommandArgumentsError
)
from dpl.things.thing import Thing, TDomainId, Connection


class AbsActuator(Thing, Actuator, State):
    """
    Actuator is an abstraction of devices that can 'act', perform some commands
    and change their states after that.

    Every actuator implementation must guarantee that:

    - it can be in one of two states: 'activated' or 'deactivated';
    - 'activation' is a switching of a device to some specific active state
      (like 'on' for LightBulb, 'opened' for Door and 'capturing' for Camera
      and 'playing' for Player);
    - 'deactivation' is a switching of a device to some specific non-active
      state (like 'off' for LightBulb, 'closed' for Door and 'idle' for Camera
      and 'stopped'/'paused' for Player);
    - it can be toggled between those to states;
    - it provides a list of available commands;
    - each available command can be executed;
    - if command can't be executed for any reason, corresponding method raises
      an exception (FIXME: CC9: or returns an error code???)
    """
    def __init__(
            self, domain_id: TDomainId,
            con_instance: Connection, con_params: dict,
            metadata: dict = None
    ):
        """
        Constructor of a Thing. Receives an instance of Connection and some
        specific parameters to use it properly. Also can receive some metadata
        to be stored like object placement, description or user-friendly name.

        :param domain_id: a unique identifier of this Thing
        :param con_instance: an instance of connection to be used
        :param con_params: parameters to access connection
        :param metadata: metadata to be stored
        """
        super().__init__(domain_id, con_instance, con_params, metadata)

        self._really_internal_state_value = self.States.unknown

    @property
    def _state(self) -> 'AbsActuator.States':
        """
        Return a really_internal_state_value

        :return: an instance of self.State
        """
        return self._really_internal_state_value

    @_state.setter
    def _state(self, new_value: 'AbsActuator.States') -> None:
        """
        Internal setter for a really_internal_state_value that can be used to
        set a new state value and update last_updated time

        :param new_value: new state value to be set
        :return: None
        """
        self._last_updated = time.time()
        self._really_internal_state_value = new_value

    @property
    def commands(self) -> Iterable[str]:
        """
        Returns a list of available commands. Must be overridden in derivative
        classes.

        :return: a tuple of command names (strings)
        """
        return 'activate', 'deactivate', 'toggle'

    # FIXME: CC9: or return an error code???
    def execute(self, command: str, args: Mapping = EMPTY_MAPPING) -> None:
        """
        Accepts the specified command on execution

        :param command: a name of command to be executed
               (see 'commands' property for a list of
                available commands)
        :param args: a mapping with keyword arguments to be
               passed on command execution
        :return: None
        :raises UnsupportedCommandError: if the specified command
                is not supported by this instance of Thing and thus
                can't be executed
        """
        if command not in self.commands:
            raise UnsupportedCommandError(
                "Unsupported command passed: {0}".format(command)
            )

        command_method = getattr(self, command)

        assert callable(command_method)

        try:
            return command_method(**args)
        except TypeError as e:
            raise UnacceptableCommandArgumentsError() from e

    def toggle(self) -> None:
        """
        Switches an object from the current state to the opposite one

        :return: None
        """
        if self.is_active:
            return self.deactivate()
        else:
            return self.activate()
