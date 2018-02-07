# Include standard modules
from typing import Iterable, Mapping

# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities.i_state import IState
from dpl.things.capabilities.i_actuator import IActuator, EMPTY_DICT
from dpl.things import Thing


class Actuator(Thing, IActuator, IState):
    """
    Actuator is an abstraction of devices that can 'act', perform some commands
    and change their states after that.

    Every actuator implementation must guarantee that:

    - it can be in one of two states: 'activated' or 'deactivated';
    - 'activation' is a switching of a device to some specific active state
      (like 'on' for LightBulb, 'opened' for Door and 'capturing' for Camera and
      'playing' for Player);
    - 'deactivation' is a switching of a device to some specific non-active state
      (like 'off' for LightBulb, 'closed' for Door and 'idle' for Camera and
      'stopped'/'paused' for Player);
    - it can be toggled between those to states;
    - it provides a list of available commands;
    - each available command can be executed;
    - if command can't be executed for any reason, corresponding method raises an
      exception (FIXME: CC9: or returns an error code???)
    """
    @property
    def commands(self) -> Iterable[str]:
        """
        Returns a list of available commands. Must be overridden in derivative classes.

        :return: a tuple of command names (strings)
        """
        return 'activate', 'deactivate', 'toggle'

    # FIXME: CC9: or return an error code???
    def execute(self, command: str, args: Mapping = EMPTY_DICT) -> None:
        """
        Accepts the specified command on execution

        :param command: a name of command to be executed
               (see 'commands' property for a list of
                available commands)
        :param args: a mapping with keyword arguments to be
               passed on command execution
        :return: None
        """
        if command not in self.commands:
            raise ValueError("Unsupported command passed: {0}".format(command))

        command_method = getattr(self, command)

        assert callable(command_method)

        return command_method(**args)

    def toggle(self) -> None:
        """
        Switches an object from the current state to the opposite one

        :return: None
        """
        if self.is_active:
            return self.deactivate()
        else:
            return self.activate()
