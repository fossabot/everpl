"""
This module contains definition of Has Volume capability
"""


class IsMuted(object):
    """
    Is Muted devices are devices that have the "is_muted" property - the
    indicator of either device was muted (i.e. has temporarily disabled
    sounding) or not.

    Actuator Is Muted devices are able to be muted
    and unmuted with ``mute`` and ``unmute`` commands correspondingly.
    """
    _capability_name = 'is_muted'
    _commands = ('mute', 'unmute')

    @property
    def is_muted(self) -> bool:
        """
        Returns if the Thing is in "muted" state.

        :return: True if the Thing was muted, False otherwise
        """
        raise NotImplementedError()
