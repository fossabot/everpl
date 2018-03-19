"""
This module contains implementation of a ActuatorDto
class and a corresponding builder to be used to
build ActuatorDto objects based on instances of Actuator

The behaviour of an ActuatorDto builder is the same as
the behaviour of a ThingDto builder. The only difference
is and addition of 'commands' and 'is_active' fields
to the ActuatorDto
"""

from .dto_builder import build_dto
from .thing_dto import ThingDto, build_thing_dto
from dpl.integrations.abs_actuator import AbsActuator


ActuatorDto = ThingDto


@build_dto.register(AbsActuator)
def _(thing: AbsActuator) -> ActuatorDto:
    result = {
        'state': thing.state.name,
        'commands': thing.commands,
        'is_active': thing.is_active
    }

    result.update(build_thing_dto(thing))

    return result
