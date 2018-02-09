from typing import Optional

from .abs_repository import AbsRepository
from dpl.model.user import User


class AbsUserRepository(AbsRepository[User]):
    """
    Pure abstract base implementation of Repository
    containing Users.

    Contains declarations of methods that must to be present
    in specific implementations of this repository
    """
    def find_by_username(self, username: str) -> Optional[User]:
        """
        Finds an instance of User by the specified username

        :param username: username of the user to be found
        :return: an instance of User with the specified
                 username or None if it wasn't found
        """
        raise NotImplementedError()
