"""
This module contains implementation of a ThingDto
class and a corresponding builder to be used to
build ThingDto objects based on instances of Thing

ThingDto for now is just a dictionary with the
following structure:

```
thing_dto_sample = {
    # a UUID-like string or other unique identifier
    "domain_id": "Li1",
    # a name of the current object state (like on and off)
    "state": "on",
    # indicates if this Thing is enabled
    "is_enabled": True,
    # indicates if this Thing is available for communication
    "is_available": True,
    # UNIX timestamp in float in UTC timezone, the time when
    # the Thing properties was last updated (changed)
    "last_updated": 1517232368.30256,
    # indicates a list of supported Capabilities
    "capabilities": ["actuator", "has_state", "is_active"]
}
```

Also all data from 'metadata' field of a Thing
will be embedded to the resulting ThingDto.

All the data provided in Capability-related fields is also embedded
to the resulting ThingDto.
"""

# FIXME: CC25: Change a set of Thing properties to eliminate
# a need in 'metadata field'
from typing import Callable, Dict

from .base_dto import BaseDto
from .dto_builder import build_dto
from dpl.things import Thing


ThingDto = BaseDto
DtoFillerType = Callable[[Thing, Dict], None]

# DTO filler registry is a mapping between the name of Capability
# and a corresponding DTO filler method (a method which receives an instance of
# Thing and adds Capability-related properties to the Thing DTO)
dto_filler_registry = dict()  # type: Dict[str, DtoFillerType]


def register_dto_filler(register_for: str) -> \
        Callable[DtoFillerType, DtoFillerType]:
    """
    register_dto_filler is a Python decorator which decorates the wrapped
    DTO Filler method in the dto_filler_registry

    :param register_for: the name of Capability which is handled by this
           callable
    :return: the same method as was specified
    """
    def _inner(wrapped: DtoFillerType) -> DtoFillerType:
        """
        Performs the real registration of the specified callable

        :param wrapped: a callable to be registered
        :return: the same callable as was specified
        """
        dto_filler_registry[register_for] = wrapped

        return wrapped

    return _inner


def build_thing_dto(thing: Thing) -> ThingDto:
    result = {
        'id': thing.domain_id,
        'is_enabled': thing.is_enabled,
        'is_available': thing.is_available,
        'last_updated': thing.last_updated,
        'capabilities': thing.capabilities
    }

    result.update(thing.metadata)

    for capability in thing.capabilities:
        dto_filler = dto_filler_registry.get(capability)

        if dto_filler is not None:
            dto_filler(thing, result)

    return result


@build_dto.register(Thing)
def _(thing: Thing) -> ThingDto:
    return build_thing_dto(thing)
