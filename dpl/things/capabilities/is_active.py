"""
This module contains definition of IsActive Capability
"""


class IsActive(object):
    """
    This interface allows a read-only access to is_active status of a Thing.

    This interface must to be provided if only only if the current state of
    a Thing can be directly stated as 'active' (i.e. working, acting, turned
    on, playing) and 'inactive' (not working, not acting, turned off, stopped).

    Otherwise it's not recommended to implement an IsActive interface.

    is_active field value if a binary value with True mapped to 'active' and
    False mapped to 'inactive'. It's recommended to map uncertain or unknown
    (null) state to the 'inactive' (False) value.

    The value of is_active field can't be directly changed by user but
    Actuators are allowed to provide some additional methods to switch between
    'active' and 'inactive' states. Also such Actuators are must to provide
    such methods as 'activate', 'deactivate' and 'toggle' to switch between the
    opposite states.

    Things are must to preserve their last known state even after
    they become unavailable. And all client classes must to be ready
    to this fact (i.e. analyze a time of the last update in last_updated
    property, analyze an availability status in is_available property
    and so on).
    """
    _capability_name = 'is_active'
    _commands = ('activate', 'deactivate', 'toggle')

    @property
    def is_active(self) -> bool:
        """
        Returns if this object is currently in one of the
        'active' states (like 'on' for lighting, 'open'
        for a door and 'playing' for player)

        :return: True if object is in any of 'active' states,
                 False otherwise
        """
        raise NotImplementedError()
