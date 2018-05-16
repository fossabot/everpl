"""
This module contains the utility functions and definition for creation
of Message instances
"""
import time
from typing import Mapping

from .message import Message, MessageFormatViolationError


def build_message(type_: str, topic: str, body: Mapping) -> Message:
    """
    Builds the new message with defined parameters. Sets the timestamp to the
    current moment of time

    :param type_: the type of the message (either "control" or "data")
    :param topic: the topic of the message
    :param body: the body, payload of the message
    :return: None
    :raises: MessageFormatViolationError - if there is an issue with one
             of the specified parameters
    """
    return Message(
        timestamp=time.time(), type_=type_,
        topic=topic, body=body
    )


def parse_message(source: Mapping) -> Message:
    """
    Parses the specified mapping and returns a corresponding message

    :param source: a mapping which represents the Message to be parsed
    :return: an instance of Message
    :raises: MessageFormatViolationError - if the specified mapping contains
             erroneous values or have some fields missing
    """
    timestamp = source.get('timestamp')
    type_ = source.get('type')
    topic = source.get('topic')
    body = source.get('body')

    return Message(
        timestamp=timestamp, type_=type_,
        topic=topic, body=body
    )
