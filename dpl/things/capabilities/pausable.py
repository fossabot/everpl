"""
This module contains definition of Pausable capability
"""
from enum import IntEnum

from .has_state import HasState


class Pausable(HasState):
    """
    Pausable devices are devices that can pause the current activity
    (i.e to temporarily stop it with keeping of a current position).
    Usually provided by some kinds of Players or Recorders. For Actuator
    Pausable Things the "pause" command can be used to pause the current
    activity (i.e. the playback, recording and so on).

    Usually implemented alongside with Play/Stop Capability.
    """
    _capability_name = 'pausable'
    _commands = ('pause',)

    class States(IntEnum):
        """
        Define a set of possible states for such devices
        """
        unknown = -1
        paused = 2
