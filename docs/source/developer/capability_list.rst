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
    :Field Description:
        Some sign of the current Thing state

:Provided Commands:
    No specific commands are provided


Has State devices are devices that have the ``state`` property. The
value of the property is some string which is directly mapped to one
of the device states. The exact set of possible states is defined by
a set of Capabilities provided by the device.


Is Active
^^^^^^^^^

:Formal Capability Name:
    ``is_active``

:Provided Fields:
    :Field Name: ``is_active``
    :Field Values:
        boolean: ``true`` or ``false``
    :Field Description:
        Signs if this Thing is in one of the "active" states.

:Provided Commands:
    :Command Name: ``activate``
    :Command Params: No params needed
    :Command Description:
        Sets this Thing to the one of the "active" states

    |

    :Command Name: ``deactivate``
    :Command Params: No params needed
    :Command Description:
        Sets this Thing to the one of the "inactive" states

    |

    :Command Name: ``toggle``
    :Command Params: No params needed
    :Command Description:
        Toggles the Thing between the opposite states. Activates
        the Thing if the current state isn't active and deactivates
        otherwise.


Has State devices are devices that have the ``state`` property. The
value of the property is some string which is directly mapped to one
of the device states. The exact set of possible states is defined by
a set of Capabilities provided by the device.


On/Off
^^^^^^

:Formal Capability Name:
    ``on_off``

:Provided Fields:
    :Field Name: ``is_power_on``
    :Field Values:
        boolean: ``true`` or ``false``
    :Field Description:
        Signs if this Thing is powered on.

:Provided Commands:
    :Command Name: ``on``
    :Command Params: No params needed
    :Command Description:
        Powers the Thing on

    |

    :Command Name: ``off``
    :Command Params: No params needed
    :Command Description:
        Powers the Thing off


On/Off devices are devices that can be either powered "on" or "off".
The current state of those devices can be determined by the value of
the ``is_power_on`` field. Actuator On/Off devices are able to be turned
on and off with the on and off commands correspondingly.

If the device provides both on_off and is_active capabilities, then
the ``on`` state is usually mapped to ``true`` value of ``is_active``
field and ``off`` state is mapped to ``false``. ``on`` command is also
mapped to the ``activate`` and ``off`` command is mapped to the
``deactivate`` command.


Open/Closed
^^^^^^^^^^^

:Formal Capability Name: ``open_closed``

:Provided Fields:
    :Field Name: ``state``
    :Field Values:
        string: ``open``, ``closed``, ``opening``, ``closing``
    :Field Description:
        Signs if this Thing (door, valve, lock, etc.) is opened,
        closed or in one of the transition states.

:Provided Commands:
    :Command Name: ``open``
    :Command Params: No params needed
    :Command Description:
        Opens the Thing

    |

    :Command Name: ``close``
    :Command Params: No params needed
    :Command Description:
        Closes the Thing


Open/Closed devices are devices that can be in either "open" or
"closed" state. The current state of those devices can be determined bу
the value of the ``state`` field. In addition to the "open" and "closed"
states there are two transitional states possible: "opening" and "closing".
Actuator Open/Closed devices are able to be opened and closed with the
``open`` and ``close`` commands correspondingly.

If the device provides both ``open_closed`` and ``is_active`` capabilities,
then the ``open`` and ``opening`` states are usually mapped to ``true``
value of ``is_active`` field and ``close`` with ``closing`` states are
mapped to ``false``. Also generic ``activate`` and ``deactivate`` commands
are available for such devices with ``activate`` mapped to ``open``,
``deactivate`` mapped to ``close`` and ``toggle`` toggles between the
opposite states (from ``open`` to ``closed``, from ``closed`` to ``open``,
from ``opening`` to ``closed``, from ``closing`` to ``opened``).


Multimode
^^^^^^^^^

:Formal Capability Name: ``multimode``

:Provided Fields:
    :Field Name: ``mode``
    :Field Values:
        The list of provided values is specified by other Capabilities
    :Field Description:
        Signs the current mode of functioning for this Thing.

:Provided Commands:
    :Command Name: ``set_mode``
    :Command Params: ``mode`` - new value for the ``mode``
    :Command Description:
        Changes the mode of functioning of this Thing to
        the specified one.


If the device provides both ``open_closed`` and ``is_active`` capabilities,
Multimode devices are able to work in different modes. By switching the mode
of the device some Capabilities may become available for usage and some may
gone. The current mode of the device is specified in the mode field. If
the mode of the device was changed, then the list of capabilities and a set
of available fields are altered to correspond to the current mode
(FIXME: Is it reasonable?). Only one device mode сan be chosen at a time.
The current mode of the device can be set via set_mode command.


Has Brightness
^^^^^^^^^^^^^^

:Formal Capability Name: ``has_brightness``

:Provided Fields:
    :Field Name: ``brightness``
    :Field Values:
        integer values in the range between 0 and 100 (including)
    :Field Description:
        Specified the current level of brightness of a Thing

:Provided Commands:
    :Command Name: ``set_brightness``
    :Command Params: ``brightness`` - the new value of brightness
    :Command Description:
        Sets the specified level of brightness for the Thing


Has Brightness devices are devices that have the ``brightness`` property.
The ``brightness`` property is an integer value in the range from
0 (zero) to 100. Actuator Has Brightness devices are able to change their
brightness with a ``set_brightness`` command. Usually normal people call
Actuator Has Brightness devices as "dimmable" devices.


Has Color HSB
^^^^^^^^^^^^^

:Formal Capability Name: ``has_color_hsb``

:Provided Fields:
    :Field Name: ``color_hue``
    :Field Values:
        An integer value between 0 and 359 including.
    :Field Description:
        Specifies the current color of a Thing in HSB format.

    |

    :Field Name: ``color_saturation``
    :Field Values:
        An integer value between 0 and 100 including.
    :Field Description:
        Specifies the current color of a Thing in HSB format.

:Provided Commands:
    :Command Name: ``set_color``
    :Command Params:
        ``hue``, ``saturation`` - the new value of hue and saturation
        correspondingly
    :Command Description:
        Sets the specified color hue and saturation for the Thing


Has Color HSB devices are devices that have the "color" property. The color
property value can be specified in HSB (hue, saturation, brightness) system.
Actuator Has Color devices are able to change their color with a set_color
command. Usually Color HSB profile is implemented by RGB Light Bulbs.


Has Color RGB
^^^^^^^^^^^^^

:Formal Capability Name: ``has_color_rgb``

:Provided Fields:
    :Field Name: ``color_rgb``
    :Field Values:
        A mapping with three keys: ``red``, ``green``, ``blue``. The value for
        each key of the RGB mapping is an integer between 0 and 255 including.
    :Field Description:
        Specifies the current color of a Thing in RGB format.

:Provided Commands:
    :Command Name: ``set_color``
    :Command Params:
        ``reg``, ``green``, ``blue`` - the values of three color components:
        red, green and blue correspondingly
    :Command Description:
        Sets the color for the Thing in RGB format.


Has Color RGB devices are devices that have the "color" property. The color
property value can be specified in RGB (red, green, blue) system.
Actuator Has Color devices are able to change their color with a set_color
command. Usually Color RGB profile is implemented by color sensors.


Has Value
^^^^^^^^^

:Formal Capability Name: ``has_value``

:Provided Fields:
    :Field Name: ``value``
    :Field Values:
        Unspecified
    :Field Description:
        Expresses some property of the Thing that can be specified as a
        single value.

:Provided Commands:
    :Command Name: ``set_value``
    :Command Params:
        Unspecified
    :Command Description:
        Sets the specified value for this Thing.


Has Value devices are devices that have the "value" property. This field and
a corresponding property is rarely used in the real life. See
``has_brightness``, ``has_temperature``, ``has_volume`` and other similar
Capabilities instead.


Has Volume
^^^^^^^^^

:Formal Capability Name: ``has_volume``

:Provided Fields:
    :Field Name: ``volume``
    :Field Values:
        The integer value between 0 and 100 including.
    :Field Description:
        The value of volume (loudness) for this Thing.

:Provided Commands:
    :Command Name: ``set_volume``
    :Command Params:
        ``volume`` - a new value of the volume for this Thing.
    :Command Description:
        Sets the specified volume (loudness level) for this Thing.


Has Value devices are devices that have the "volume" property - the measure
of loudness of how loud its sound is. Volume is an integer value in the range
from 0 (zero) to 100. Actuator Has Volume devices are able to change their
volume with a ``set_volume`` command.

