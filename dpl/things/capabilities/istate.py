from enum import Enum


class IState(object):
    """
    This interface allows a read-only access to states of a Thing.

    All implementations of this interface must to have a 'state'
    property and declare a concrete list (enumeration) of all
    states possible
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