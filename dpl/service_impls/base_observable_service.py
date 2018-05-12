import weakref
from typing import TypeVar, MutableSet, Optional, Generic

from dpl.utils.observer import Observer
from dpl.dtos.base_dto import BaseDto
from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity

from dpl.services.observable_service import ObservableService, ServiceEventType
from .base_service import BaseService


TStored = TypeVar('TStored', bound=BaseEntity)
TEntityDto = TypeVar('TEntityDto', bound=BaseDto)


class BaseObservableService(
    BaseService[TStored],
    ObservableService[TEntityDto],
    Generic[TStored, TEntityDto]
):
    """
    Base implementation of the ObservableService interface
    """
    def __init__(self):
        """
        Constructor. Initializes an empty set of observers
        """
        self._observers = set()  # type: MutableSet[Observer]
        self._weak_self = weakref.proxy(self)

    def subscribe(self, observer: Observer) -> None:
        """
        Adds the specified Observer to the list of subscribers

        :param observer: an instance of Observer to be added
        :return: None
        """
        self._observers.add(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """
        Removes the specified  Observer from the list of subscribers

        :param observer: an instance of Observer to be deleted
        :return: None
        """
        self._observers.discard(observer)

    def _notify(
            self, object_id: TDomainId, event_type: ServiceEventType,
            object_dto: Optional[TEntityDto]
    ) -> None:
        """
        Notifies all of the subscribers that an object, controlled by this
        Service, was modified, added to or deleted from the system

        :param object_id: an identifier of an altered object
        :param event_type: enum value, specifies what happened to the object
        :param object_dto: a DTO of the altered object or None if it was
               deleted
        :return: None
        """
        for o in self._observers:
            o.update(
                source=self._weak_self,
                event_type=event_type,
                object_id=object_id,
                object_dto=object_dto
            )
