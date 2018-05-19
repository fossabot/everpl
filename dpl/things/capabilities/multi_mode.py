"""
This module contains a definition of Multi-Mode Thing Capability
"""

from typing import Iterable


class MultiMode(object):
    """
    Multi-Mode Thing Capability indicates an ability of a Thing to work in one
    of the preliminarily defined modes. For example, a TV can work as a monitor
    with multiple inputs, as a Streaming device with a lot of channels, as a
    Media Player which plays files from USB storage or network and so on.

    It's expected that Multi-Mode devices can work only in one mode at a time.
    The current mode of functioning is specified in the ``current_mode`` field.
    The list of all available modes is specified in the ``available_modes``
    field. For Actuator devices it's possible to switch between modes using
    the ``set_mode`` command.
    """
    _capability_name = 'multi_mode'
    _commands = ('set_mode',)

    @property
    def current_mode(self) -> str:
        """
        Indicates the current mode of functioning for this Thing

        :return: the current mode of functioning for this Thing
        """
        raise NotImplementedError()

    @property
    def available_modes(self) -> Iterable[str]:  # Collection[str]
        """
        Indicates the list of all available modes of functioning for this Thing

        :return: the list of all available modes of functioning for this Thing
        """
        raise NotImplementedError()
