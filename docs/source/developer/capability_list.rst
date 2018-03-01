.. _possible_capabilities:

Possible Capabilities
=====================

So, here is the list of all Capabilities possible in the system.


Actuators
^^^^^^^^^

:Formal Capability Name:
    ``actuator``

:Provided Fields:
    No fields provided

:Provided Commands:
    The list of provided commands is specified by other Capabilities


Actuators are devices that can "act", i.e. execute some commands,
to change their state and the state of the outside world. For those
devices the ``/execute`` endpoint is available in REST API and the
corresponding ``execute`` method is available in the internal
representation of a Thing.

All Things that are able to execute some commands must to support an
``actuator`` capability. Otherwise all commands, even if they are
specified in "Provided Commands" section of this documentation, are
supposed to be unavailable.


Has State
^^^^^^^^^

:Formal Capability Name:
    ``has_state``

:Provided Fields:
    :Field Name: ``state``
    :Field Values:
        The set of possible values is specified by other Capabilities

:Provided Commands:
    No specific commands are provided


Has State devices are devices that have the ``state`` property. The
value of the property is some string which is directly mapped to one
of the device states. The exact set of possible states is defined by
a set of Capabilities provided by the device.



