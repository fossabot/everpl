# Include standard modules
from enum import IntEnum

# Include 3rd-party modules
# Include DPL modules
from .abs_togglable_actuator import AbsTogglableActuator
from dpl.things.capabilities import PlayStop, IsActive


class AbsPlayer(AbsTogglableActuator, PlayStop, IsActive):
    """
    Player is an abstraction of basic player device or application. It can be
    in one of two states: 'stopped' and 'playing'.
    """
    class States(IntEnum):
        unknown = -1
        playing = 1
        stopped = 0

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
        Switches an object to the inactive ('stopped') state

        :return: None
        """
        return self.stop()

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
