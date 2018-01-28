"""
Contains a pure abstract (interface-like) base implementation
of repository
"""

from typing import TypeVar, Generic, Sequence, Optional


# FIXME: CC22: Use UUID instead of string as a domain ID
TDomainId = str
TStored = TypeVar('TStored')


class AbsRepository(Generic[TStored]):
    """
    Pure abstract base implementation of Repository.

    Contains declarations of methods that must to be present
    in all derivative implementations of repositories
    """
    def count(self) -> int:
        """
        Counts a number of elements stored in this repository

        :return: integer, a number of elements stored in this
                 repository
        """
        raise NotImplementedError()

    # FIXME: CC23: Use database_id instead of domain_id
    def load(self, domain_id: TDomainId) -> Optional[TStored]:
        """
        Loads a single object from an internal storage by its
        identifier or None (null) if it wasn't found

        :param domain_id: an identifier of an object
        :return: an object itself or None if it wasn't found
        """
        raise NotImplementedError()

    def load_all(self) -> Sequence[TStored]:
        """
        Returns all objects that are stored in this Repository

        :return: a collection of stored objects
        """
        raise NotImplementedError()

    def select_all_domain_ids(self) -> Sequence[TDomainId]:
        """
        Returns a collection of identifiers of all objects
        stored in this Repository

        :return: a collection of identifiers
        """
        raise NotImplementedError()

    def add(self, new_obj: TStored) -> None:
        """
        Add a new element to the storage

        :param new_obj: new object to be stored
        :return: None
        """
        raise NotImplementedError()

    def delete(self, domain_id: TDomainId) -> None:
        """
        Removes an element with the specified ID from the
        storage

        :param domain_id: an ID of element to be removed
        :return: None
        """
        raise NotImplementedError()

    # FIXME: CC24: Add definitions of commit, rollback and
    # start_transaction methods
