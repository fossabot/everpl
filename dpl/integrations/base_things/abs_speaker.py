# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import HasVolume, IsMuted
from .abs_on_off import AbsOnOff


class AbsSpeaker(AbsOnOff, HasVolume, IsMuted):
    """
    AbsSpeaker is an abstraction of all Speakers - sound producing devices
    with a single input source. The only thing they can do is to be turned on,
    off and regulate their volume (i.e. the level of loudness).

    Please note that muted devices and devices with a volume set to zero
    are still considered as "active" devices. So, Speakers are considered
    to be in "active" state until they are not powered off.
    """
    _type = "speaker"

    def set_volume(self, volume: int) -> None:
        """
        Sets the specified volume (loudness level) for this Thing.

        :param volume: a new value of the volume for this Thing in the range
               from 0 to 100 including.
        :return: None
        """
        raise NotImplementedError()

    def mute(self) -> None:
        """
        Mutes the Thing.

        :return: None
        """
        raise NotImplementedError()

    def unmute(self) -> None:
        """
        Unmutes the Thing - moves the Thing from a “muted” state.

        :return: None
        """
        raise NotImplementedError()
