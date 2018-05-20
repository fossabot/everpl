"""
This package contains definitions of base (abstract) implementations of Things,
recommended to be used by developers of integrations
"""


from .abs_value_sensor import AbsValueSensor
from .abs_binary_sensor import AbsBinarySensor
from .abs_button import AbsButton
from .abs_switch import AbsSwitch
from .abs_contact_sensor import AbsContactSensor
from .abs_temp_sensor import AbsTemperatureSensor

from .abs_actuator import (
    AbsActuator, UnsupportedCommandError, UnacceptableCommandArgumentsError
)
from .abs_on_off import AbsOnOff
from .abs_open_closed import AbsOpenClosed
from .abs_togglable_actuator import AbsTogglableActuator
from .abs_lock import AbsLock
from .abs_door_actuator import AbsDoorActuator
from .abs_shades import AbsShades
from .abs_light import AbsLight
from .abs_dimmable_light import AbsDimmableLight
from .abs_ct_light import AbsColorTemperatureLight
from .abs_color_light import AbsColorLight
from .abs_power_switch import AbsPowerSwitch
from .abs_valve import AbsValve
from .abs_fan import AbsFan
from .abs_vs_fan import AbsVariableSpeedFan
from .abs_player import AbsPlayer
from .abs_pausable_player import AbsPausablePlayer
from .abs_track_player import AbsTrackPlayer
from .abs_speaker import AbsSpeaker
from .abs_speaker_system import AbsSpeakerSystem


__all__ = (
    'AbsValueSensor', 'AbsBinarySensor', 'AbsButton', 'AbsSwitch',
    'AbsContactSensor', 'AbsTemperatureSensor',

    'UnsupportedCommandError', 'UnacceptableCommandArgumentsError',
    'AbsActuator', 'AbsOnOff', 'AbsOpenClosed', 'AbsTogglableActuator',

    'AbsLock', 'AbsDoorActuator', 'AbsShades', 'AbsLight',
    'AbsDimmableLight', 'AbsColorTemperatureLight', 'AbsColorLight',
    'AbsPowerSwitch', 'AbsValve', 'AbsFan', 'AbsVariableSpeedFan',
    'AbsPlayer', 'AbsPausablePlayer', 'AbsTrackPlayer',
    'AbsSpeaker', 'AbsSpeakerSystem'
)
