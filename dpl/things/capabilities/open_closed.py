from enum import Enum

from .has_state import HasState


class OpenClosed(HasState):
    """
    Open/Closed devices are devices that can be in either "open" or
    "closed" state. The current state of those devices can be determined bу
    the value of the ``state`` field. In addition to the "open" and "closed"
    states there are two transitional states possible: "opening" and "closing".

    Actuator Open/Closed devices are MUST to implement to ``open`` and
    ``close`` commands to open or close a Thing correspondingly.

    If the device provides both ``open_closed`` and ``is_active`` capabilities,
    then the ``open`` and ``opening`` states are usually mapped to ``true``
    value of ``is_active`` field and ``close`` with ``closing`` states are
    mapped to ``false``. Also generic ``activate`` and ``deactivate`` commands
    are available for such devices with ``activate`` mapped to ``open``,
    ``deactivate`` mapped to ``close`` and ``toggle`` toggles between the
    opposite states (from ``open`` to ``closed``, from ``closed`` to ``open``,
    from ``opening`` to ``closed``, from ``closing`` to ``opened``).
    """
    class States(Enum):
        """
        Possible states of the thing: 'open', 'closed' and 'unknown'.
        """
        closed = 0b00
        opening = 0b01
        closing = 0b10
        opened = 0b11
        unknown = None

    # Everything else is inherited from HasState Capability
