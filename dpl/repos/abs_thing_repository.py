from typing import Optional

from .observable_repository import ObservableRepository, TDomainId
from dpl.things import Thing


class AbsThingRepository(ObservableRepository[Thing]):
    """
    Pure abstract base implementation of Repository
    containing Things.

    Contains declarations of methods that must to be present
    in specific implementations of this repository
    """
    def select_by_placement(self, placement_id: Optional[TDomainId]):  # -> Collection[Thing]:
        """
        Fetches a collection of identifiers of all Things
        that are present in the specified placement

        :param placement_id: an identifier of Placement to be
               used for filtering; None (null) can be used as
               a value of parameter to fetch a list of Things
               that don't belong to any Placement
        :return: a collection of Things that belong to the
                 specified placement
        """
        raise NotImplementedError()

    def select_by_connection(self, connection_id: TDomainId):  # -> Collection[Thing]:
        """
        Fetches a collection of identifiers of all Things that
        use the specified Connection

        :param connection_id: an ID of Connection of interest
        :return: a collection of all Things that use the
                 specified connection
        """
        raise NotImplementedError()
