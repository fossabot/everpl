# Include standard modules
from typing import Iterable, Mapping

# Include 3rd-party modules
from dpl.utils.empty_mapping import EMPTY_MAPPING

# Include DPL modules
from dpl.things.capabilities.has_state import HasState
from dpl.things.capabilities.actuator import (
    Actuator,
    UnsupportedCommandError,
    UnacceptableCommandArgumentsError
)
from dpl.things.thing import Thing, TDomainId, Connection
from dpl.things.commands_filler_meta import CommandsFiller


class AbsActuator(
    Thing, Actuator, HasState, metaclass=CommandsFiller
):
    """
    AbsActuator is a base implementation of Actuator interface. Such actuators
    always have a set of available commands and usually have some state
    associated with them.

    It's expected that all derivative classes will just implement methods and
    properties that are specific for concrete Thing type while the base
    implementation or properties and commands will be left unchanged. But it's
    not obligatorily if the derivative class will manage all the functionality
    by itself (i.e. will notify all the subscribers on changes, implement all
    declared properties and methods and so on).
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
        self._really_internal_state_value = new_value
        self._apply_update()

    @property
    def commands(self) -> Iterable[str]:
        """
        Returns a list of available commands.

        By default the list of available commands is fetched from the
        _all_commands private property, filled by a metaclass. So, by default,
        all commands declared in inherited Capabilities will be listed.

        Derivative classes are allowed to override this method.

        :return: a tuple of command names (strings)
        """
        return self._all_commands

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
