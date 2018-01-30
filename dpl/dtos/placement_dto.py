"""
This module contains implementation of a PlacementDto
class and a corresponding builder to be used to
build PlacementDto objects based on instances of Placement

PlacementDto for now is just a dictionary with the
following structure:

```
placement_dto_sample = {
    # a UUID-like string or other unique identifier
    "domain_id": "R1",
    # a user-friendly name for this Placement
    "friendly_name": "Corridor",
    # a URL of an image used which corresponds to this Placement
    "image_url": "https://lampydomowe.pl/blog/wp-content/uploads/2017/09/furniture-382154_1920-1024x611.jpg"
}
```

"""


from .base_dto import BaseDto
from .dto_builder import build_dto
from dpl.placements import Placement


PlacementDto = BaseDto


@build_dto.register(Placement)
def _(placement: Placement) -> PlacementDto:
    return {
        'domain_id': placement.domain_id,
        'friendly_name': placement.friendly_name,
        'image_url': placement.image_url
    }
