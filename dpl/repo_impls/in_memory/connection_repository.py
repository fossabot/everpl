from dpl.repos.abs_connection_repository import AbsConnectionRepository, Connection
from .base_repository import BaseRepository


class ConnectionRepository(BaseRepository[Connection], AbsConnectionRepository):
    """
    An implementation of in-memory storage of Connections
    """
    pass
