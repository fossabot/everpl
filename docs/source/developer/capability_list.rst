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


Is Active devices are devices that have the ``is_active`` property.
The value of this property is a boolean with ``true`` mapped to the
set of "active" states (i.e. working, acting, turned on) and ``false``
mapped to the set of "inactive" states (i.e. not working, not acting,
turned off, stopped).

Is Active Capability must to be implemented if and only if the current
state of the device can be clearly mapped to either "active" or
"inactive" state.

Actuator Is Active devices must to implement such methods as ``toggle``,
``activate`` and ``deactivate``.


On/Off
^^^^^^

:Formal Capability Name:
    ``on_off``

:Provided Fields:
    :Field Name: ``is_powered_on``
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
the ``is_powered_on`` field. Actuator On/Off devices are able to be turned
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
        string: ``opened``, ``closed``, ``opening``, ``closing``
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


Open/Closed devices are devices that can be in either "opened" or
"closed" state. The current state of those devices can be determined bу
the value of the ``state`` field. In addition to the "opened" and "closed"
states there are two transitional states possible: "opening" and "closing".
Actuator Open/Closed devices are able to be opened and closed with the
``open`` and ``close`` commands correspondingly.

If the device provides both ``open_closed`` and ``is_active`` capabilities,
then the ``open`` and ``opening`` states are usually mapped to ``true``
value of ``is_active`` field and ``close`` with ``closing`` states are
mapped to ``false``. Also generic ``activate`` and ``deactivate`` commands
are available for such devices with ``activate`` mapped to ``open``,
``deactivate`` mapped to ``close`` and ``toggle`` toggles between the
opposite states (from ``opened`` to ``closed``, from ``closed`` to ``opened``,
from ``opening`` to ``closed``, from ``closing`` to ``opened``).


Multi-Mode
^^^^^^^^^^

:Formal Capability Name: ``multi_mode``

:Provided Fields:
    :Field Name: ``current_mode``
    :Field Values:
        A string from of the ``available_modes`` list
    :Field Description:
        Signs the current mode of functioning for this Thing.

    |

    :Field Name: ``available_modes``
    :Field Values:
        List of strings
    :Field Description:
        Signs all available modes of functioning for this Thing.

:Provided Commands:
    :Command Name: ``set_mode``
    :Command Params: ``mode`` - new value for the ``mode``
    :Command Description:
        Changes the mode of functioning of this Thing to
        the specified one.


Multi-Mode devices are able to work in different modes. By switching the mode
of the device some Capabilities may become available for usage and some may
gone. The current mode of the device is specified in the mode field. If
the mode of the device was changed, then the list of capabilities and a set
of available fields are altered to correspond to the current mode
(FIXME: Is it reasonable?). Only one device mode сan be chosen at a time.
The current mode of the device can be set via set_mode command. All available
device modes are listed in ``available_modes`` field. The content of
``available_modes`` list is defined by Thing Type and provided Capabilities.


Has Brightness
^^^^^^^^^^^^^^

:Formal Capability Name: ``has_brightness``

:Provided Fields:
    :Field Name: ``brightness``
    :Field Values:
        floating point values in the range between 0.0 and 100.0 (including)
    :Field Description:
        Specified the current level of brightness of a Thing

:Provided Commands:
    :Command Name: ``set_brightness``
    :Command Params: ``brightness`` - the new value of brightness
    :Command Description:
        Sets the specified level of brightness for the Thing


Has Brightness devices are devices that have the ``brightness`` property.
The ``brightness`` property is a floating point value in the range from
0.0 (zero) to 100.0. Actuator Has Brightness devices are able to change their
brightness with a ``set_brightness`` command. Usually normal people call
Actuator Has Brightness devices "dimmable" devices.


Has Color HSB
^^^^^^^^^^^^^

:Formal Capability Name: ``has_color_hsb``

:Provided Fields:
    :Field Name: ``color_hue``
    :Field Values:
        A floating point value between 0.0 including and
        360.0 not including.
    :Field Description:
        Specifies the current color of a Thing in HSB format.

    |

    :Field Name: ``color_saturation``
    :Field Values:
        An floating-point value between 0.0 and 100.0 including.
    :Field Description:
        Specifies the current color of a Thing in HSB format.

:Provided Commands:
    :Command Name: ``set_color``
    :Command Params:
        ``hue``, ``saturation`` - the new values of hue and saturation
        correspondingly
    :Command Description:
        Sets the specified color hue and saturation for the Thing.
        Brightness must to be set separately, see `Has Brightness`_
        Capability description for details.


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


Has Color Temperature
^^^^^^^^^^^^^^^^^^^^^

:Formal Capability Name: ``has_color_temp``

:Provided Fields:
    :Field Name: ``color_temp``
    :Field Values:
        Integer between 1000 and 10000 including. Color temperature value,
        expressed in Kelvins.
    :Field Description:
        Specifies the current color temperature of a Thing in Kelvins.

:Provided Commands:
    :Command Name: ``set_color_temp``
    :Command Params:
        ``color_temp`` - the new value of color temperature to be set.
    :Command Description:
        Sets the color temperature for a Thing.


Color Temperature devices are devices that have the "color temperature"
property. The color temperature is expressed in Kelvins and can take integer
values from 1000 to 10000 including. The color temperature of light source
or other Actuator can be set with ``set_color_temp`` command. If the Thing
doesn't support specified color temperature value (i.e. it's too low or
too high for this Thing), then the color temperature will be set to the nearest
supported value. For example, the minimum value is 2000 and the maximum value
is 6500 K for majority of light bulbs available on the market. It's recommended
for client applications to put some marks on the scale for Warm White (2700 K),
Cool White (4000 K) and Daylight (5000 K) values.


Has Temperature
^^^^^^^^^^^^^^^

:Formal Capability Name: ``has_temperature``

:Provided Fields:
    :Field Name: ``temperature_c``
    :Field Values:
        Floating point, temperature in degrees of **Celsius**.
    :Field Description:
        Expresses the current temperature measured by a Thing.

:Provided Commands:
    No commands provided


Has Temperature devices are devices that have the "temperature" property.
The value of "temperature_c" property is expressed in degrees of Celsius,
Fahrenheits are not supported for now.

It's supposed that the value of "temperature" property can'be changed by
user and represents the current, real temperature of controlled object.
For other purposes, please refer to Capability and Thing types which
provide a "target_temperature" property.


Has Position
^^^^^^^^^^^^

:Formal Capability Name: ``has_position``

:Provided Fields:
    :Field Name: ``position``
    :Field Values:
        Floating point number which represents the position of an object
        in numbers from 0.0 to 100.0 including.
    :Field Description:
        Expresses the current position of a Thing.

:Provided Commands:
    :Command Name: ``set_position``
    :Command Params:
        ``position`` - the new value of position to be set.
    :Command Description:
        Sets the new position for a Thing.


Has Position devices are devices that have the "position" property.
This property allows to set a position of an object using only one
single dimension. For example, it can represent the position of
a shade (50% unrolled, 20% of window covered, etc.), the width of
an opening (for gates, sliding doors, valves) and so on.


Fan Speed
^^^^^^^^^

:Formal Capability Name: ``fan_speed``

:Provided Fields:
    :Field Name: ``fan_speed``
    :Field Values:
        Floating point numbers from 0.0 to 100.0 including.
    :Field Description:
        Expresses the current fan rotation speed in percents.

:Provided Commands:
    :Command Name: ``set_fan_speed``
    :Command Params:
        ``fan_speed`` - the new value of fan speed to be set.
    :Command Description:
        Sets the new fan speed for a Thing.


Fan Speed devices are devices that have a build-in and externally
controllable (at least monitored) fan. For example, that can be
heaters, some HVACs and fans itself (as separate devices).

The speed of some fans can be changed only by a constant step.
For such cases (for example, for table fans with only 3 speeds),
the whole range will be separated on the corresponding number
of segments. For example, it'll be 0-25, 26-50, 51-75 and 76-100
for a generic fan with speeds 0 (stopped), 1, 2 and 3 correspondingly.


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


Play/Stop
^^^^^^^^^

:Formal Capability Name: ``play_stop``

:Provided Fields:
    :Field Name: ``state``
    :Field Values:
        string: ``playing``, ``stopped``
    :Field Description:
        Signs if the playback for this Thing (for some kind of player)
        is in progress (playing) or stopped.

:Provided Commands:
    :Command Name: ``play``
    :Command Params: No params needed
    :Command Description:
        Starts the playback.

    |

    :Command Name: ``stop``
    :Command Params: No params needed
    :Command Description:
        Stops the playback.

Play/Stop devices are devices that can play some media (i.e. music, video,
radio, media stream, etc.) and which have basic controls for playback.
Uses the "state" field to define the current playback state and corresponding
commands to stop and resume playback.


Pausable
^^^^^^^^

:Formal Capability Name: ``pausable``

:Provided Fields:
    :Field Name: ``state``
    :Field Values:
        string: ``paused``
    :Field Description:
        Signs if the activity for this Thing (playing, recording, etc.)
        is paused.

:Provided Commands:
    :Command Name: ``pause``
    :Command Params: No params needed
    :Command Description:
        Pauses the current activity.

Pausable devices are devices that can pause the current activity
(i.e to temporarily stop it with keeping of a current position).
Usually provided by some kinds of Players or Recorders. For Actuator
Pausable Things the "pause" command can be used to pause the current
activity (i.e. the playback, recording and so on).

Usually implemented alongside with Play/Stop Capability.


Track Switching
^^^^^^^^^^^^^^^

:Formal Capability Name: ``track_switching``

:Provided Fields:
    No fields provided

:Provided Commands:
    :Command Name: ``next``
    :Command Params: No params needed
    :Command Description:
        Switches the playback to the next track, video or stream.

    |

    :Command Name: ``previous``
    :Command Params: No params needed
    :Command Description:
        Switches the playback to the previous track, video or stream.

Track Switching devices are devices that can switch between the current,
previous and the next track, song, file, video or stream in the playback
queue. Usually implemented by Players. Track Switching devices aren't
obliged to support playlists, switching to specific tracks in the queue
and so on. For support of the mentioned features please refer to the
corresponding Capabilities.

Usually implemented alongside with Play/Stop and Pausable Capabilities.


Track Info
^^^^^^^^^^

:Formal Capability Name: ``track_info``

:Provided Fields:
    :Field Name: ``track_info``
    :Field Values:
        String
    :Field Description:
        Contains the information about a current playing song, movie,
        stream or another media in a form of a single human-readable
        string.

:Provided Commands:
    No commands provided

Track Info devices are devices that can display information about the
current playing media. The type of this information can be arbitrary
and is not specified by this document. It's not even supposed to be
parsed by other devices. The only thing that must to be granted is that
the track_info field value must to be human-readable without any additional
processing.

For support of information about the song name, movie name, artists,
current playing TV program and so on please refer to the corresponding
Capabilities and Thing types.


Has Volume
^^^^^^^^^^

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


Is Muted
^^^^^^^^

:Formal Capability Name: ``is_muted``

:Provided Fields:
    :Field Name: ``is_muted``
    :Field Values:
        boolean: ``true`` or ``false``
    :Field Description:
        Indicates if the Thing was muted.

:Provided Commands:
    :Command Name: ``mute``
    :Command Params:
        No params needed
    :Command Description:
        Mutes the Thing.

    |

    :Command Name: ``unmute``
    :Command Params:
        No params needed
    :Command Description:
        Unmutes the Thing - moves the Thing from a "muted" state.


Is Muted devices are devices that have the "is_muted" property - the
indicator of either device was muted (i.e. has temporarily disabled
sounding) or not. Actuator Is Muted devices are able to be muted
and unmuted with ``mute`` and ``unmute`` commands correspondingly.


Multi-Source
^^^^^^^^^^^^

:Formal Capability Name: ``multi_source``

:Provided Fields:
    :Field Name: ``current_source``
    :Field Values:
        An integer value, an index of the current source from the
        ``available_sources`` list.
    :Field Description:
        Contains an identifier of the source which is currently chosen.

    |

    :Field Name: ``available_sources``
    :Field Values:
        An ordered list of strings.
    :Field Description:
        An list of human-readable names for all available sources.

:Provided Commands:
    :Command Name: ``set_source``
    :Command Params:
        ``source`` - a new value for the ``current_source`` field.
    :Command Description:
        Sets the specified source for this Thing.


Multi-Source devices are devices that can play, display or use in any
other way information from one of several information sources. The good
example of such device is a computer monitor. Computer monitor often
can display information from several inputs as HDMI, VGA or DisplayPort
input. Or a speaker system which can play a sound from coaxial, optical,
HDMI, Bluetooth or AUX inputs.

For such devices as TVs, home theaters and other multi-functional devices
please refer to the Multi-Mode_ Capability documentation.
