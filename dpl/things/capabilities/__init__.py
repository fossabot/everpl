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
from .has_value import HasValue


__all__ = (
    'Actuator', 'HasState', 'HasValue', 'IsActive',
    'OnOff', 'OpenClosed', 'HasValue'
)
