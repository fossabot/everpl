# Include standard modules
import unittest
from enum import Enum
import json
from typing import Type

# Include 3rd-party modules
# Include DPL modules
from dpl.utils.json_enum_encoder import JsonEnumEncoder


class SampleEnum(Enum):
    open = 0
    closed = 1
    unknown = None


def is_serialization_correct(serializer: Type[json.JSONEncoder], value: Enum):
    """
    Tries to serialize an Enum member and deserialize it back.
    Checks if Enum member was serialized to string which contains
    a name of this Enum member.

    :param serializer: an instance of JSONEncoder to be used for serialization
    :param value: a value (Enum member) to be tested
    :return: True if serialized value is a name of Enum member, false otherwise
    """
    assert isinstance(value, Enum)
    assert issubclass(serializer, json.JSONEncoder)

    serialized = json.dumps(value, cls=serializer)
    deserialized = json.loads(serialized)

    return deserialized == value.name


class MyTestCase(unittest.TestCase):
    def test_encoder(self):
        """
        Tests that all members of Enumeration are serialized to their names

        :return: None
        """
        for i in SampleEnum:
            self.assertTrue(
                is_serialization_correct(serializer=JsonEnumEncoder, value=i)
            )

if __name__ == '__main__':
    unittest.main()
