# Include standard modules
from enum import IntEnum

# Include 3rd-party modules
# Include DPL modules
from .abs_player import AbsPlayer
from dpl.things.capabilities import Pausable


class AbsPausablePlayer(AbsPlayer, Pausable):
    """
    Player is an abstraction of basic player device or application. It can be
    in one of three states: 'stopped', 'playing' and 'paused'.
    """
    _type = "pausable_player"

    class States(IntEnum):
        unknown = -1
        playing = 1
        stopped = 0
        paused = 2

    def deactivate(self) -> None:
        """
        Switches an object to the inactive ('paused') state

        :return: None
        """
        return self.pause()

    def pause(self) -> None:
        """
        Pause playing and switches the object to the 'paused' state.

        :return: None
        """
        raise NotImplementedError()
