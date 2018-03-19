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
    "last_updated": 1517232368.30256
}
```

Also all data from 'metadata' field of a Thing
will be embedded to the resulting ThingDto
"""

# FIXME: CC25: Change a set of Thing properties to eliminate
# a need in 'metadata field'


from .base_dto import BaseDto
from .dto_builder import build_dto
from dpl.things import Thing


ThingDto = BaseDto


def build_thing_dto(thing: Thing) -> ThingDto:
    result = {
        'id': thing.domain_id,
        'is_enabled': thing.is_enabled,
        'is_available': thing.is_available,
        'last_updated': thing.last_updated
    }

    result.update(thing.metadata)

    return result


@build_dto.register(Thing)
def _(thing: Thing) -> ThingDto:
    return build_thing_dto(thing)
