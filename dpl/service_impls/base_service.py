"""
This module contains a definition of a useful class
called BaseService. This class provides methods to
resolve objects stored in Repositories and raises an
exception if an object can't be found
"""

from typing import TypeVar, Generic, Optional
from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity
from dpl.services.service_exceptions import ServiceEntityResolutionError
from dpl.repos.abs_repository import AbsRepository


TStored = TypeVar('TStored', bound=BaseEntity)


class BaseService(Generic[TStored]):
    """
    A base class for all service implementations.
    Provides only two private methods: resolve_entity
    and check_resolved
    """
    def _resolve_entity(self, repository: AbsRepository, domain_id: TDomainId) -> TStored:
        """
        Resolves an entity object by the specified ID

        :param repository: a source container for resolving
        :param domain_id: ID of object to be fetched
        :return: an instance of BaseEntity from the repository
        """
        entity = repository.load(domain_id)  # type: TStored

        self._check_resolved(entity)

        return entity

    @staticmethod
    def _check_resolved(resolved: Optional[BaseEntity]) -> None:
        """
        Checks that the resolved entity is not None
        (i.e. that the entity was found)

        :param resolved: an instance of entity object to be checked
        :return: None
        :raises ServiceEntityResolutionError: if the specified object
                is None
        """
        if resolved is None:
            raise ServiceEntityResolutionError()
