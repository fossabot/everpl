"""
This module contains implementation of a ConnectionDto
class and a corresponding builder to be used to
build ConnectionDto objects based on instances of Connection

ConnectionDto for now is just a dictionary with the
following structure:

```
connection_dto_sample = {
    # a UUID-like string or other unique identifier
    "domain_id": "C1"

    # ... and nothing more (for now)
}
```
"""


from .base_dto import BaseDto
from .dto_builder import build_dto
from dpl.connections import Connection


ConnectionDto = BaseDto


@build_dto.register(Connection)
def _(connection: Connection) -> ConnectionDto:
    return {
        'domain_id': connection.domain_id
    }
