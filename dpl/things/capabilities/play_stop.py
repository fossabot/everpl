"""
This module contains definition of Play/Stop capability
"""
from enum import IntEnum

from .has_state import HasState


class PlayStop(HasState):
    """
    Play/Stop devices are devices that can play some media (i.e. music, video,
    radio, media stream, etc.) and which have basic controls for playback.
    Uses the "state" field to define the current playback state and
    corresponding commands to stop and resume playback.
    """
    _capability_name = 'play_stop'
    _commands = ('play', 'stop')

    class States(IntEnum):
        """
        Define a set of possible states for such devices
        """
        unknown = -1
        playing = 1
        stopped = 0
