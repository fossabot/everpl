from .abs_repository import AbsRepository
from dpl.connections import Connection


class AbsConnectionRepository(AbsRepository[Connection]):
    """
    Pure abstract base implementation of Repository
    containing Connections.

    Contains declarations of methods that must to be present
    in specific implementations of this repository
    """
    pass
