# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from .abs_pausable_player import AbsPausablePlayer
from dpl.things.capabilities import TrackSwitching, TrackInfo


class AbsTrackPlayer(AbsPausablePlayer, TrackSwitching, TrackInfo):
    """
    Track Player type represents all devices with an ability to switch between
    tracks: backward and forward. It inherits all the fields and behaviour
    provided by Pausable Player type but adds two additional commands:
    "next" and "previous".

    Also, there is new field "track_info" added that allows to find general
    information about the current playing audio track, video, station or
    stream.
    """
    _type = "track_player"

    def next(self) -> None:
        """
        Switches to the next track in playback queue

        :return: None
        """
        raise NotImplementedError()

    def previous(self) -> None:
        """
        Switches to the previous track in playback queue

        :return: None
        """
        raise NotImplementedError()
