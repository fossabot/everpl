"""
This module contains a builder function used to build
a new DTO (data transfer object) based on the class of
the passed object
"""

from functools import singledispatch
from typing import Any

from .base_dto import BaseDto


@singledispatch
def build_dto(object_instance: Any) -> BaseDto:
    """
    Builder function. Lookups for an appropriate DTO
    builder method for a specified instance based on
    its type and returns a built DTO based on it

    :param object_instance: instance which contains
           data to be stored in DTO
    :return: a build DTO instance
    :raises NotImplementedError: if the implementation
            of a builder function wasn't found for the
            specified instance
    """
    raise NotImplementedError(
        'No builder method found for this type of '
        'objects: %s' % object_instance
    )
