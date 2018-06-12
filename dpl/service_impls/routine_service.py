import logging
from typing import Mapping, MutableMapping, MutableSet

from dpl.model.domain_id import TDomainId
from dpl.routines.routine import Routine
from dpl.routines.condition import ConditionalOperator
from dpl.repos.abs_routine_repo import AbsRoutineRepo
from dpl.services.abs_routine_service import AbsRoutineService
from dpl.services.abs_thing_service import (
    AbsThingService, ServiceEntityResolutionError, ServiceInvalidArgumentsError
)
from dpl.events.event_hub import EventHub
from dpl.events.event import Event
from dpl.events.object_related_event import ObjectRelatedEvent

from .base_service import BaseService


LOGGER = logging.getLogger(__name__)


class RoutineService(AbsRoutineService, BaseService[Mapping]):  # BaseService[RoutineDTO]
    def __init__(
            self, routine_repo: AbsRoutineRepo, thing_service: AbsThingService
    ):
        self._routines = routine_repo
        self._thing_service = thing_service

        self._routine_topics = dict()  # type: MutableMapping[str, MutableSet[TDomainId]]

        for routine in self._routines.load_all():
            for topic in routine.sensitivity_list:
                related = self._routine_topics.setdefault(topic, set())
                related.add(routine.domain_id)

    def enable(self, routine_id: TDomainId):
        routine = self._resolve_entity(self._routines, routine_id)
        routine.is_enabled = True

    def disable(self, routine_id: TDomainId):
        routine = self._resolve_entity(self._routines, routine_id)
        routine.is_enabled = False

    def update(self, source: EventHub, *args, **kwargs):
        n_of_args = len(args) + len(kwargs)

        if n_of_args > 1:
            raise ValueError("Unexpected number of arguments")

        if n_of_args == 0:
            raise ValueError("event argument must to be specified")

        event = kwargs.get(args[0])  # type: Event

        if isinstance(event, ObjectRelatedEvent):
            self._process_event(event)
        else:
            LOGGER.debug(
                "Unexpected event type: ignoring, %s, %s", type(event), event
            )

    def _process_event(self, event: ObjectRelatedEvent):
        related = self._routine_topics.get(event.topic)

        if related is None:
            return

        for routine_id in related:
            routine = self._routines.load(routine_id)  # type: Routine
            condition = routine.condition

            check_thing_dto = self._thing_service.view(condition.thing_id)

            if condition.field_name not in check_thing_dto:
                LOGGER.error(
                    "Field from the routine condition was not found: "
                    "%s, %s, %s", routine_id, condition.thing_id,
                    condition.field_name
                )
                continue

            thing_current_value = check_thing_dto[condition.field_name]

            if self._compare(
                    thing_current_value, condition.field_value,
                    condition.operator
            ):
                self.execute_commands(routine)


    @staticmethod
    def _compare(value1, value2, op: ConditionalOperator) -> bool:
        if op is ConditionalOperator.EQ:
            return value1 == value2
        elif op is ConditionalOperator.GE:
            return value1 >= value2
        elif op is ConditionalOperator.GT:
            return value1 > value2
        else:
            raise NotImplementedError("Unknown operator")

    def execute_commands(self, routine: Routine):
        actions = routine.actions

        for action in actions:
            try:
                self._thing_service.send_command(
                    to_actuator_id=action.thing_id,
                    command=action.command,
                    command_args=action.command_args
                )
            except ServiceEntityResolutionError:
                LOGGER.error(
                    "Failed to resolve Thing %s from routine: %s",
                    action.thing_id, routine.domain_id
                )
            except ServiceInvalidArgumentsError:
                LOGGER.error(
                    "Failed to execute action %s for Thing %s from routine %s:"
                    " unacceptable arguments %s",
                    action.command, action.thing_id, routine.domain_id,
                    action.command_args
                )
            except Exception as e:
                LOGGER.error(
                    "Failed to execute a %s routine action %s for Thing %s: "
                    "%s, %s", routine.domain_id, action.command,
                    action.thing_id, type(e), e
                )

