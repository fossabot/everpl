"""
This module contains implementation of a SessionDto
class and a corresponding builder to be used to
build SessionDto objects based on instances of User.

SessionDto is just a dictionary which contains the
specified set of fields:

- domain_id - an unique identifier of this object;
- time_created - timestamp of when the Session was
  created (float, UNIX time);
- user_id - an identifier of User for which the Session
  was requested to be created;
- client_info - an information about a device or
  application which requested creation of this Session
  (like a content of a User-Agent header);
- client_ip - an IP address of a device which requested
  creation of this Session.

access_token parameter is considered as private and
is not available in SessionDto.
"""

from .base_dto import BaseDto
from .dto_builder import build_dto
from dpl.auth.session import Session

SessionDto = BaseDto


@build_dto.register(Session)
def _(session: Session) -> SessionDto:
    return {
        'domain_id': session.domain_id,
        'time_created': session.time_created,
        'user_id': session.user_id,
        'client_info': session.client_info,
        'client_ip': session.client_ip,
    }

