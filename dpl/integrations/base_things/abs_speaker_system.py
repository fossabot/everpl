# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things.capabilities import HasVolume, IsMuted
from .abs_on_off import AbsOnOff


class AbsSpeakerSystem(AbsOnOff, HasVolume, IsMuted):
    """
    AbsSpeaker is an abstraction of all sound speakers and
    speaker systems that have multiple input sources.

    In addition to the
    base functionality of a Speaker, such devices allow to view, choose and
    change the sound source from the list of provided sources.
    """
    _type = "speaker_system"

    def set_source(self, source: int) -> None:
        """
        Allows to choose a current source of sound (sound input) by its
        identifier (index) from a list of available source.

        :param source: an identifier of a sound source to be chosen
        :return: None
        """
        raise NotImplementedError()

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
