"""
This module contains a definition of a base Service class
"""
from typing import TypeVar

from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity
from .service_exceptions import ServiceEntityLinkError
from .observable_service import ObservableService


TEntityDto = TypeVar('TEntityDto', bound=BaseEntity)


class AbsEntityService(ObservableService[TEntityDto]):
    """
    Entity Service implements two basic operations for all
    Entities in the system:

    - fetching a full list of DTOs of all stored objects
    - fetching of data transfer object for an Entity by its ID
    """
    def view_all(self):  # -> Collection[TEntityDto]:
        """
        Fetch a full list of DTOs of all stored objects

        :return: a collection of DTOs
        """
        raise NotImplementedError()

    def view(self, domain_id: TDomainId) -> TEntityDto:
        """
        Fetch a DTO of stored object by the ID specified

        :param domain_id: id of object to be fetched
        :return: a DTO of stored object
        :raises ServiceResolutionError: if the entity with
                the specified ID can't be found
        """
        raise NotImplementedError()

    def remove(self, domain_id: TDomainId) -> None:
        """
        REMOVES an Entity with the specified ID altogether
        from the system

        :param domain_id: an identifier of Entity to be deleted
        :return: None
        :raises ServiceResolutionError: if the entity with
                the specified ID can't be found
        :raises ServiceEntityLinkError: if the specified can't
                be removed because some other entity is linked
                (uses or refers) to it
        """
        raise NotImplementedError()
