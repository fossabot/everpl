from enum import IntEnum


class HasState(object):
    """
    This interface allows a read-only access to states of a Thing.

    All implementations of this interface must to have a 'state'
    property and declare a concrete list (enumeration) of all
    states possible.

    Also it's needed to mention that if the device provides both ``has_state``
    and ``is_active`` capabilities, than all of its states can be mapped
    onto two big categories of states: either "active" or "inactive" states.
    In such case, an additional ``is_active`` field is provided. For more
    information, see documentation for IsActive capability and docs for
    specific device type or implementation.

    'unknown' state is considered as an 'inactive' binary state.

    Things are must to preserve their last known state even after
    they become unavailable. And all client classes must to be ready
    to this fact (i.e. analyze a time of the last update in last_updated
    property, analyze an availability status in is_available property
    and so on).
    """
    _capability_name = 'has_state'

    class States(IntEnum):
        """
        Possible states of the thing. Must be overridden in derived
        classes with 'unknown' state preserved
        """
        unknown = -1

    @property
    def state(self) -> 'States':
        """
        Return a current state of the Thing

        :return: an instance of self.State
        """
        raise NotImplementedError()
