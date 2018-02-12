"""
This module contains implementation of a UserDto
class and a corresponding builder to be used to
build UserDto objects based on instances of User.

UserDto is just a dictionary which contains the
specified set of fields:

- domain_id - an unique identifier of this object;
- username - some name used by user for logging in
  and to be displayed in UI
"""

from .base_dto import BaseDto
from .dto_builder import build_dto
from dpl.model.user import User

UserDto = BaseDto


@build_dto.register(User)
def _(user: User) -> UserDto:
    return {
        'domain_id': user.domain_id,
        'username': user.username
    }

