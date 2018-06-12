from typing import Optional, Mapping, Any, Iterable

from dpl.model.domain_id import TDomainId
from dpl.dtos.thing_dto import ThingDto
from .service_exceptions import (
    ServiceEntityResolutionError,
    ServiceTypeError,
    ServiceInvalidArgumentsError,
    ServiceUnsupportedCommandError
)
from .abs_entity_service import AbsEntityService

from dpl.repos.abs_routine_repo import AbsRoutineRepo


class AbsRoutineService(AbsEntityService):
    def create_routine(self, *args, **kwargs):
        raise NotImplementedError()

    def change_sensitivity_list(
            self, routine_id: TDomainId, new_list: Iterable[str]
    ):
        raise NotImplementedError()

    def change_target_thing(
            self, routine_id: TDomainId, new_thing_id: TDomainId
    ):
        raise NotImplementedError()

    def enable(self, routine_id: TDomainId):
        raise NotImplementedError()

    def disable(self, routine_id: TDomainId):
        raise NotImplementedError()

    def change_actions(
            self, routine_id: TDomainId,
            new_actions: Iterable[Mapping]  # Iterable[ActionDTO]
    ):
        raise NotImplementedError()

    def change_condition(
            self, routine_id: TDomainId, new_condition: Mapping  # ConditionDTO
    ):
        raise NotImplementedError()

    def change_friendly_name(
            self, routine_id: TDomainId, new_name: Optional[str]
    ):
        raise NotImplementedError()

    def select_by_author(self, author_id: TDomainId):  # Collection[RoutineDTO]
        raise NotImplementedError()
