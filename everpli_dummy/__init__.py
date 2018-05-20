"""
Dummy integration contains a reference implementations of all thing types.
Those reference implementations just print some data on display in a response
to sent commands and use DummyConnection connection type.
"""

from .dummy_connection import DummyConnection
from .dummy_switch import DummySwitch
from .dummy_slider import DummySlider
from .dummy_pausable_player import DummyPausablePlayer

__all__ = ["DummyConnection", "DummySwitch", "DummySlider",
           "DummyPausablePlayer"]
