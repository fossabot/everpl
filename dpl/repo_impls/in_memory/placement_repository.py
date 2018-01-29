from dpl.repos.abs_placement_repository import AbsPlacementRepository, Placement
from .base_repository import BaseRepository


class PlacementRepository(BaseRepository[Placement], AbsPlacementRepository):
    """
    An implementation of in-memory storage of Placements
    """
    pass
