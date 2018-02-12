from typing import Optional

from dpl.model.user import User
from dpl.repos.abs_user_repository import AbsUserRepository

from .db_session_manager import DbSessionManager
from .base_repository import BaseRepository


class UserRepository(BaseRepository[User], AbsUserRepository):
    """
    An implementation of SQLAlchemy-based storage
    of userRepository
    """
    def __init__(self, session_manager: DbSessionManager):
        """
        Constructor. Receives an instance of SessionManager
        to be used and saves a link to it to the internal
        variable.

        :param session_manager: an instance of SessionManager
               to be used for requesting SQLAlchemy Sessions

        """
        super().__init__(
            session_manager=session_manager,
            stored_cls=User
        )

    def find_by_username(self, username: str) -> Optional[User]:
        """
        Finds an instance of User by the specified username

        :param username: username of the user to be found
        :return: an instance of User with the specified
                 username or None if it wasn't found
        """
        return self._session.query(self._stored_cls).filter_by(_username=username).one_or_none()
