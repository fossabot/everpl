"""
This module contains functions for construction of ObjectRelatedEvents based on
on a data sent by ObservableServices
"""
from typing import Optional

from dpl.model.domain_id import TDomainId
from dpl.dtos.base_dto import BaseDto
from dpl.services.observable_service import ObservableService, ServiceEventType
from .topic import iterable_to_topic
from .object_related_event import ObjectRelatedEvent


def build_object_related_event(
        source: ObservableService,
        object_id: TDomainId, event_type: ServiceEventType,
        object_dto: Optional[BaseDto],
        *,
        target_root_topic: str
) -> ObjectRelatedEvent:
    """
    Builds an instance of ObjectRelatedEvent based on data received from
    an ObservableService

    :param source: source of the event
    :param object_id: an identifier of an altered object
    :param event_type: enum value, specifies what happened to the object
    :param object_dto: a DTO of the altered object or None if it was deleted
    :param target_root_topic: a root topic to be used for construction
    :return: an instance of ObjectRelatedEvent
    """
    assert isinstance(source, ObservableService)

    last_topic_part = event_type.name
    topic_parts = (target_root_topic, object_id, last_topic_part)
    topic = iterable_to_topic(topic_parts)

    event = ObjectRelatedEvent(
        topic=topic,
        object_dto=object_dto
    )

    return event
