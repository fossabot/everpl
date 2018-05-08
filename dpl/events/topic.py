"""
This module contains methods for working with topics
"""

import typing


def topic_to_list(topic: str) -> typing.List[str]:
    """
    Converts the specified topic to the corresponding list

    :param topic: a tuple to be converted
    :return: a tuple which corresponds to the specified topic
    """
    return topic.split('/')


def iterable_to_topic(iterable: typing.Iterable[str]) -> str:
    """
    Converts a content of iterable to the topic string

    :param iterable: an iterable to be converted
    :return: topic as a string
    """
    return '/'.join(iterable)
