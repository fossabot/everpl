"""
This module contains a definition of Message - of a base class for all messages
transreceived via Streaming API connection.
"""
from typing import Mapping, Type, Union, Any, Optional


class MessageFormatViolationError(Exception):
    """
    An exception to be raised if at least one of the Message fields has an
    invalid type or value. The name of the field, text message, the expected
    and received values are specified in the corresponding parameters.
    """
    def __init__(
            self, violated_field: str, expected: Union[type, str],
            actual: Union[type, str], message: str = None
    ):
        """
        Constructor. Saves the data about the occurred error to the
        corresponding fields

        :param violated_field: the name of the field which format was violated
        :param expected: the expected type or value for the field
        :param actual: the received (actual) type or value for the field
        :param message: a message which describes the issue
        """
        self.violated_field = violated_field
        self.expected = expected
        self.received = actual
        self.message = message


def validate_type(field_name: str, field_value: Any, expected_type: Type):
    """
    Validates that the specified field_value has the specified type. Raises
    an exception otherwise

    :param field_name: the name of the field to be validated
    :param field_value: the value of the field to be validated
    :param expected_type: the expected type of the field value
    :return: None
    :raises: MessageFormatViolationError - if the specified field value has
             a type different from expected
    """
    if not isinstance(field_value, expected_type):
        raise MessageFormatViolationError(
            violated_field=field_name,
            expected=expected_type,
            actual=type(field_value),
            message="Invalid field type"
        )


def validate_message(timestamp: float, type_: str, topic: str, body: Mapping):
    """
    Performs the validation of the specified message content

    :param timestamp: the moment of creation of this Message in UNIX time
           format with floating point
    :param type_: the type of the message (either "control" or "data")
    :param topic: the topic of the message
    :param body: the body, payload of the message
    :return: None
    :raises: MessageFormatViolationError - if there is an issue with one of the
             specified parameters
    """
    validate_type(
        field_name="timestamp",
        field_value=timestamp,
        expected_type=float
    )

    validate_type(
        field_name="type",
        field_value=type_,
        expected_type=str
    )

    if type_ not in ("control", "data"):
        raise MessageFormatViolationError(
            violated_field="type", expected="\"control\" or \"data\"",
            actual=type_,
            message="Invalid field value"
        )

    validate_type(
        field_name="topic",
        field_value=topic,
        expected_type=str
    )

    validate_type(
        field_name="body",
        field_value=body,
        expected_type=Mapping
    )


class Message(object):
    """
    Message. Defines the structure of a typical message transreceived via
    Streaming API
    """
    def __init__(
            self, timestamp: float, type_: str, topic: str, body: Mapping,
            message_id: int = None
    ):
        """
        Constructor. Sets values of the properties to the specified values

        :param timestamp: the moment of creation of this Message in UNIX time
               format with floating point
        :param type_: the type of the message (either "control" or "data")
        :param topic: the topic of the message
        :param body: the body, payload of the message
        :param message_id: a lifetime identifier of this message; can't
               be changed once set
        :raises: MessageFormatViolationError - if there is an issue with one
                 of the specified parameters
        """
        validate_message(timestamp, type_, topic, body)

        self._timestamp = timestamp
        self._type = type_
        self._topic = topic
        self._body = body
        self._message_id = message_id

    @property
    def timestamp(self) -> float:
        """
        Returns the moment of creation of this Message in UNIX time format

        :return: the moment of creation of this Message
        """
        return self._timestamp

    @property
    def type(self) -> str:
        """
        Returns the type of this Message: either "control" or "data"

        :return: the type of this Message: either "control" or "data"
        """
        return self._type

    @property
    def topic(self) -> str:
        """
        Returns the topic of this Message - the string formatted as
        "here/is/your/topic"

        :return: the topic of this Message
        """
        return self._topic

    @property
    def body(self) -> Mapping:
        """
        Returns the body (payload) of this Message

        :return: the body (payload) of this Message
        """
        return self._body

    @property
    def message_id(self) -> Optional[int]:
        """
        Returns the current message identifier - a lifetime identifier of this
        Message (if if was be set). Is present only for Tracked Messages

        :return: the current message identifier if it was set
        """
        return self._message_id

    @message_id.setter
    def message_id(self, new_value: int):
        """
        Sets the lifetime message identifier for this Message. Can be set only
        once. Raises ValueError otherwise

        :param new_value: a new value to be set
        :return: None
        :raises ValueError: if an identifier was already set
        """
        self._message_id = new_value
