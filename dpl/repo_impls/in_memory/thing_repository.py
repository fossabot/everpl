from typing import Optional, Sequence, MutableSequence

from dpl.model.domain_id import TDomainId
from dpl.things.thing import Thing
from .base_repository import BaseRepository
from dpl.repos.abs_thing_repository import AbsThingRepository


class ThingRepository(BaseRepository[Thing], AbsThingRepository):
    """
    An implementation of Things storage
    """

    def select_by_placement(self, placement_id: Optional[TDomainId]) -> Sequence[TDomainId]:
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
        # FIXME: Replace by native database filtering when DB
        # of settings will be added
        result = list()  # type: MutableSequence[TDomainId]

        for thing in self._objects.values():
            if thing.metadata.get('placement') == placement_id:
                result.append(thing.domain_id)

        return result

    def select_by_connection(self, connection_id: TDomainId) -> Sequence[TDomainId]:
        """
        Fetches a collection of identifiers of all Things that
        use the specified Connection

        :param connection_id: an ID of Connection of interest
        :return: a collection of identifiers of all Things that
                 use the specified connection
        """
        # FIXME: Replace by native database filtering when DB
        # of settings will be added
        result = list()  # type: MutableSequence[TDomainId]

        for thing in self._objects.values():
            if thing.metadata.get('con_id') == connection_id:
                result.append(thing.domain_id)

        return result
