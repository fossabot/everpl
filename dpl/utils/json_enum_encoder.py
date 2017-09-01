# Include standard modules
import json
from enum import Enum
from typing import Any

# Include 3rd-party modules
# Include DPL modules


class JsonEnumEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> str:
        """
        Redefine 'default' method of JSONEncoder:
            if object is enum variable - use it's name as value
            else - try to serialize with default json encoder

        :param obj: object to be serialized
        :return: a string representation of specified object
        """
        if isinstance(obj, Enum):
            return obj.name

        return json.JSONEncoder.default(self, obj)
