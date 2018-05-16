"""
This module contains utility classes and functions for converting of Messages
to JSON-serializable objects
"""
import functools
from json import JSONEncoder, dumps
from typing import Mapping

from .message import Message


class MessageJSONEncoder(JSONEncoder):
    """
    Encodes instances of Message to JSON-serializable objects (mappings)
    """
    def default(self, o: Message) -> Mapping:
        """
        Implements the conversion of Messages into Mappings

        :param o: an object to be converted
        :return: the result of conversion
        """
        result = {
            'timestamp': o.timestamp,
            'type': o.type,
            'topic': o.topic,
            'body': o.body
        }

        if o.message_id is not None:
            result["message_id"] = o.message_id

        return result


message_dumps = functools.partial(dumps, cls=MessageJSONEncoder)
