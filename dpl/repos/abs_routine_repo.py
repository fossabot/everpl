from dpl.model.domain_id import TDomainId

from dpl.routines.routine import Routine
from .abs_repository import AbsRepository


class AbsRoutineRepo(AbsRepository):
    def select_by_author(self, author_id: TDomainId):  # -> Collection[ThingSettings]:
        raise NotImplementedError()
