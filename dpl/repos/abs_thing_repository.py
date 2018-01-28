from typing import Optional, TypeVar

from .abs_repository import AbsRepository, TDomainId
from dpl.things import Thing


TThing = TypeVar('TThing', bound=Thing)


class AbsThingRepository(AbsRepository[TThing]):
    """
    Pure abstract base implementation of Repository
    containing Things.

    Contains declarations of methods that must to be present
    in specific implementations of this repository
    """
    def select_by_placement(self, placement_id: Optional[TDomainId]):  # -> Collection[TDomainId]:
        """
        Fetches a collection of identifiers of all Things
        that are present in the specified placement

        :param placement_id: an identifier of Placement to be
               used for filtering; None (null) can be used as
               a value of parameter to fetch a list of Things
               that don't belong to any Placement
        :return: a collection of identifiers of all things that
                 belong to the specified placement
        """
        raise NotImplementedError()

    def select_by_connection(self, connection_id: TDomainId):  # -> Collection[TDomainId]:
        """
        Fetches a collection of identifiers of all Things that
        use the specified Connection

        :param connection_id: an ID of Connection of interest
        :return: a collection of identifiers of all Things that
                 use the specified connection
        """
        raise NotImplementedError()
