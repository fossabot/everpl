from .abs_repository import AbsRepository
from dpl.placements import Placement


class AbsPlacementRepository(AbsRepository[Placement]):
    """
    Pure abstract base implementation of Repository
    containing Placements.

    Contains declarations of methods that must to be present
    in specific implementations of this repository
    """
    pass
