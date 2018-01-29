from typing import TypeVar, Optional, MutableMapping, ValuesView, AbstractSet

from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity
from dpl.repos.abs_repository import AbsRepository


TEntity = TypeVar("TEntity", bound=BaseEntity)
TEntityCollection = MutableMapping[TDomainId, TEntity]


class BaseRepository(AbsRepository[TEntity]):
    """
    A base implementation of in-memory repository
    """
    def __init__(self):
        """
        Constructor. Initializes internal in-memory storage
        """
        self._objects = dict()  # type: TEntityCollection
        self._sample = {'key': 12344}

    def count(self):
        """
        Counts a number of elements stored in this repository

        :return: integer, a number of elements stored in this
                 repository
        """
        return len(self._objects)

    def load(self, domain_id: TDomainId) -> Optional[TEntity]:
        """
        Loads a Thing from internal storage and returns it
        by its identifier

        :param domain_id: an ID of Thing to fetched
        :return: a Thing with a corresponding identifier
                 or None (null) if it wasn't found
        """
        return self._objects.get(domain_id, None)

    def load_all(self) -> ValuesView[TEntity]:
        """
        Returns all Things that are stored in this Repository

        :return: a collection of stored objects
        """
        # FIXME: PyCharm complains on the following file.
        # But type hints for derivative collections like
        # ThingRepository work just fine. Maybe, issue PY-25832
        # is related to this problem. OR maybe I really wrote
        # something erroneous here
        return self._objects.values()

    def select_all_domain_ids(self) -> AbstractSet[TDomainId]:
        """
        Returns all Things that are stored in this Repository

        :return: a collection of stored objects
        """
        return self._objects.keys()

    def add(self, new_obj: TEntity) -> None:
        """
        Add a new element to the storage

        :param new_obj: new object to be stored
        :return: None
        """
        domain_id = new_obj.domain_id

        self._objects[domain_id] = new_obj

    def delete(self, domain_id: TDomainId) -> None:
        """
        Removes an element with the specified ID from the
        storage

        :param domain_id: an ID of element to be removed
        :return: None
        """
        self._objects.pop(domain_id)
