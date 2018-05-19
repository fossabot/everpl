"""
This module contains definition of Multi-Source capability
"""
from typing import Tuple


class MultiSource(object):
    """
    Multi-Source devices are devices that can play, display or use in any
    other way information from one of several information sources.
    """
    _capability_name = 'multi_source'
    _commands = ('set_source',)

    @property
    def current_source(self) -> int:
        """
        Returns an identifier (index) of the source which is currently chosen
        from the list of sources defined in ``available_sources`` property.

        :return: an identifier of the source which is currently chosen.
        """
        raise NotImplementedError()

    @property
    def available_sources(self) -> Tuple[str]:
        """
        Returns an ordered list of human-readable names of all
        available sources.

        :return: an ordered list of human-readable names of sources.
        """
        raise NotImplementedError()
