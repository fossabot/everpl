# Include standard modules
from enum import Enum
from typing import Tuple

# Include 3rd-party modules
# Include DPL modules
from .abs_actuator import AbsActuator


class AbsPlayer(AbsActuator):
    """
    Player is an abstraction of basic player device or application. It can be
    in one of three states: 'stopped', 'playing' and 'paused'.
    """
    class States(Enum):
        stopped = 0
        playing = 1
        paused  = 2
        unknown = None

    @property
    def commands(self) -> Tuple[str, ...]:
        """
        Returns a list of available commands. Must be overridden in derivative
        classes.

        :return: a tuple of command names (strings)
        """
        return super().commands + ('stop', 'play', 'pause')

    @property
    def is_active(self):
        """
        Indicates if the object is in active state

        :return: True if state == 'on', false otherwise
        """
        return self.state == self.States.playing

    def activate(self) -> None:
        """
        Switches an object to the active ('playing') state

        :return: None
        """
        return self.play()

    def deactivate(self) -> None:
        """
        Switches an object to the inactive ('paused') state

        :return: None
        """
        return self.pause()

    def play(self, *args, **kwargs) -> None:
        """
        Starts playing and switches the object to the 'playing' state.
        Additional parameters like track name or URL can be provided.

        :param args: positional parameters
        :param kwargs: keyword parameters
        :return: None
        """
        raise NotImplementedError()

    def stop(self) -> None:
        """
        Stops playing and switches the object to the 'stopped' state.

        :return: None
        """
        raise NotImplementedError()

    def pause(self) -> None:
        """
        Pause playing and switches the object to the 'paused' state.

        :return: None
        """
        raise NotImplementedError()
