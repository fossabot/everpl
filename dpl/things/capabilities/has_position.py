"""
This module contains definition of Has Position capability
"""


class HasPosition(object):
    """
    Has Position devices are devices that have the "position" property.
    This property allows to set a position of an object using only one
    single dimension. For example, it can represent the position of
    a shade (50% unrolled, 20% of window covered, etc.), the width of
    an opening (for gates, sliding doors, valves) and so on.
    """
    _capability_name = 'has_position'
    _commands = ('set_position',)

    @property
    def position(self) -> float:
        """
        Returns the current position of a Thing in values from 0.0 to 100.0.

        :return: the current position of a Thing
        """
        raise NotImplementedError()
