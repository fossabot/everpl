from enum import Enum


class IState(object):
    """
    This interface allows a read-only access to states of a Thing.

    All implementations of this interface must to have a 'state'
    property and declare a concrete list (enumeration) of all
    states possible.

    Also it's needed to mention that all states must to be clearly
    mapped to a one of a binary states: either 'active' or 'inactive'.
    Such binary representation of a state can be read from an
    'is_active' property. And different Actuators can provide own
    methods for switching between an active and inactive states.

    'unknown' state is considered as an 'inactive' binary state.

    Things are must to preserve their last known state even after
    they become unavailable. And all client classes must to be ready
    to this fact (i.e. analyze a time of the last update in last_updated
    property, analyze an availability status in is_available property
    and so on).
    """
    class States(Enum):
        """
        Possible states of the thing. Must be overridden in derived
        classes with 'unknown' state preserved
        """
        unknown = None

    @property
    def state(self) -> 'States':
        """
        Return a current state of the Thing

        :return: an instance of self.State
        """
        raise NotImplementedError()
