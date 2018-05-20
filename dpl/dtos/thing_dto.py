"""
This module contains implementation of a ThingDto
class and a corresponding builder to be used to
build ThingDto objects based on instances of Thing

ThingDto for now is just a dictionary with the
following structure:

```
thing_dto_sample = {
    # a UUID-like string or other unique identifier
    "domain_id": "Li1",
    # a name of the current object state (like on and off)
    "state": "on",
    # indicates if this Thing is enabled
    "is_enabled": True,
    # indicates if this Thing is available for communication
    "is_available": True,
    # UNIX timestamp in float in UTC timezone, the time when
    # the Thing properties was last updated (changed)
    "last_updated": 1517232368.30256,
    # indicates a list of supported Capabilities
    "capabilities": ["actuator", "has_state", "is_active"]
}
```

Also all data from 'metadata' field of a Thing
will be embedded to the resulting ThingDto.

All the data provided in Capability-related fields is also embedded
to the resulting ThingDto.
"""

# FIXME: CC25: Change a set of Thing properties to eliminate
# a need in 'metadata field'
from typing import Callable, Dict

from .base_dto import BaseDto
from .dto_builder import build_dto
from dpl.things import Thing, capabilities


ThingDto = BaseDto
DtoFillerType = Callable[[Thing, Dict], None]

# DTO filler registry is a mapping between the name of Capability
# and a corresponding DTO filler method (a method which receives an instance of
# Thing and adds Capability-related properties to the Thing DTO)
dto_filler_registry = dict()  # type: Dict[str, DtoFillerType]


def register_dto_filler(register_for: str) -> \
        Callable[[DtoFillerType], DtoFillerType]:
    """
    register_dto_filler is a Python decorator which decorates the wrapped
    DTO Filler method in the dto_filler_registry

    :param register_for: the name of Capability which is handled by this
           callable
    :return: the same method as was specified
    """
    def _inner(wrapped: DtoFillerType) -> DtoFillerType:
        """
        Performs the real registration of the specified callable

        :param wrapped: a callable to be registered
        :return: the same callable as was specified
        """
        dto_filler_registry[register_for] = wrapped

        return wrapped

    return _inner


def build_thing_dto(thing: Thing) -> ThingDto:
    result = {
        'id': thing.domain_id,
        'is_enabled': thing.is_enabled,
        'is_available': thing.is_available,
        'last_updated': thing.last_updated,
        'capabilities': thing.capabilities
    }

    result.update(thing.metadata)

    for capability in thing.capabilities:
        dto_filler = dto_filler_registry.get(capability)

        if dto_filler is not None:
            dto_filler(thing, result)

    return result


@build_dto.register(Thing)
def _(thing: Thing) -> ThingDto:
    return build_thing_dto(thing)


# FIXME: CC39: Define such DTO fillers in their own or Capability-related
# modules


@register_dto_filler('actuator')
def _(thing: capabilities.Actuator, result: ThingDto) -> None:
    result['commands'] = thing.commands


@register_dto_filler('has_state')
def _(thing: capabilities.HasState, result: ThingDto) -> None:
    result['state'] = thing.state.name


@register_dto_filler('is_active')
def _(thing: capabilities.IsActive, result: ThingDto) -> None:
    result['is_active'] = thing.is_active


@register_dto_filler('on_off')
def _(thing: capabilities.OnOff, result: ThingDto) -> None:
    result['is_powered_on'] = thing.is_powered_on


@register_dto_filler('has_value')
def _(thing: capabilities.HasValue, result: ThingDto) -> None:
    result['value'] = thing.value


@register_dto_filler('multi_mode')
def _(thing: capabilities.MultiMode, result: ThingDto) -> None:
    result['current_mode'] = thing.current_mode
    result['available_modes'] = thing.available_modes


@register_dto_filler('has_brightness')
def _(thing: capabilities.HasBrightness, result: ThingDto) -> None:
    result['brightness'] = thing.brightness


@register_dto_filler('has_color_hsb')
def _(thing: capabilities.HasColorHSB, result: ThingDto) -> None:
    result['color_hue'] = thing.color_hue
    result['color_saturation'] = thing.color_saturation


@register_dto_filler('has_color_rgb')
def _(thing: capabilities.HasColorRGB, result: ThingDto) -> None:
    # pylint: disable=W0212
    # noinspection PyProtectedMember
    result['color_rgb'] = thing.color_rgb._asdict()


@register_dto_filler('has_color_temp')
def _(thing: capabilities.HasColorTemperature, result: ThingDto) -> None:
    result['color_temp'] = thing.color_temp


@register_dto_filler('has_temperature')
def _(thing: capabilities.HasTemperature, result: ThingDto) -> None:
    result['temperature_c'] = thing.temperature_c


@register_dto_filler('has_position')
def _(thing: capabilities.HasPosition, result: ThingDto) -> None:
    result['position'] = thing.position


@register_dto_filler('fan_speed')
def _(thing: capabilities.FanSpeed, result: ThingDto) -> None:
    result['fan_speed'] = thing.fan_speed


@register_dto_filler('track_info')
def _(thing: capabilities.TrackInfo, result: ThingDto) -> None:
    result['track_info'] = thing.track_info


@register_dto_filler('has_volume')
def _(thing: capabilities.HasVolume, result: ThingDto) -> None:
    result['volume'] = thing.volume


@register_dto_filler('is_muted')
def _(thing: capabilities.IsMuted, result: ThingDto) -> None:
    result['is_muted'] = thing.is_muted


@register_dto_filler('multi_source')
def _(thing: capabilities.MultiSource, result: ThingDto) -> None:
    result['available_sources'] = thing.available_sources
    result['current_source'] = thing.current_source
