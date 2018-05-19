"""
This package contains definitions of different capabilities,
different interfaces like a set of properties and methods,
that can be provided by different implementations of a Thing
"""

from .actuator import Actuator
from .has_state import HasState
from .is_active import IsActive
from .on_off import OnOff
from .open_closed import OpenClosed
from .multi_mode import MultiMode
from .has_brightness import HasBrightness
from .has_color_hsb import HasColorHSB
from .has_color_rgb import HasColorRGB
from .has_value import HasValue
from .has_volume import HasVolume


__all__ = (
    'Actuator', 'HasState', 'IsActive',
    'OnOff', 'OpenClosed', 'MultiMode',
    'HasBrightness', 'HasColorHSB', 'HasColorRGB',
    'HasValue', 'HasVolume'
)
