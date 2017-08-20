# Include standard modules
from typing import Tuple

# Include 3rd-party modules
# Include DPL modules
from dpl.connections import Connection
from dpl.things import Thing


class Actuator(Thing):
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
    def commands(self) -> Tuple[str, ...]:
        """
        Returns a list of available commands. Must be overridden in derivative classes.
        :return: a tuple of command names (strings)
        """
        return 'activate', 'deactivate', 'toggle'

    @property
    def is_active(self) -> bool:
        """
        Returns an activation flag
        :return: true if object is in any 'active' state, false otherwise
        """
        raise NotImplementedError

    # FIXME: CC9: or return an error code???
    def execute(self, command: str, *args, **kwargs) -> None:
        """
        Executes a command with 'command' name and specified arguments
        :param command: a name of command to be executed
        :param args: positional arguments to be passed
        :param kwargs: keyword arguments to be passed
        :return: None
        """
        if command not in self.commands:
            raise ValueError("Unsupported command passed: {0}".format(command))

        command_method = getattr(self, command)

        assert callable(command_method)

        return command_method(*args, **kwargs)

    def activate(self) -> None:
        """
        Turns an object to some specific 'active' state
        :return: None
        """
        raise NotImplementedError

    def deactivate(self) -> None:
        """
        Turns an object to some specific 'inactive' state
        :return: None
        """
        raise NotImplementedError

    def toggle(self) -> None:
        """
        Switches an object from the current state to the opposite one
        :return: None
        """
        if self.is_active:
            return self.activate()
        else:
            return self.deactivate()
