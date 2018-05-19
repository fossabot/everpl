"""
This module contains definition of Track Switching capability
"""
from .actuator import Actuator


class TrackSwitching(Actuator):
    """
    Track Switching devices are devices that can switch between the current,
    previous and the next track, song, file, video or stream in the playback
    queue. Usually implemented by Players. Track Switching devices aren't
    obliged to support playlists, switching to specific tracks in the queue
    and so on. For support of the mentioned features please refer to the
    corresponding Capabilities.

    Usually implemented alongside with Play/Stop and Pausable Capabilities.

    """
    _capability_name = 'track_switching'
    _commands = ('next', 'previous')
