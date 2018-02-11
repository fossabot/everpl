from dpl.repos.abs_placement_repository import AbsPlacementRepository, Placement

from .db_session_manager import DbSessionManager
from .base_repository import BaseRepository


class PlacementRepository(BaseRepository[Placement], AbsPlacementRepository):
    """
    An implementation of SQLAlchemy-based storage
    of Placements
    """
    def __init__(self, session_manager: DbSessionManager):
        """
        Constructor. Receives an instance of SessionManager
        to be used and saves a link to it to the internal
        variable.

        :param session_manager: an instance of SessionManager
               to be used for requesting SQLAlchemy Sessions
        """
        super().__init__(session_manager, stored_cls=Placement)
