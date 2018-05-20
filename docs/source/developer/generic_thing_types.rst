Generic Thing Types
-------------------

While talking about Things, the two important field was mentioned: a "type"
field and a "capabilities" field.

A "capabilities" field was discussed earlier in detail , in :doc:`./capabilities`
section of documentation. Capabilities define what devices are capable of, what
such devices can do and provide.

But the meaning of a "type" field was left almost not discussed. This flaw will
be fixed below, in Generic Thing Types section of documentation


General Information
===================

There is huge variety of Things available on the market. There are some crazy
devices that combine functions of a light bulb and a speaker [#f1]_, toaster and
printer [#f2]_, or Bluetooth-enabled toasters [#f3]_, or fridges with Tizen
onboard [#f4]_...

But most of the time, it's possible to pick out a primary functionality of
a device and thus classify it to one of generic, common device types. And this,
in turn, allows developers to provide the most relevant information to the user.
At least, a appropriate device icon :).

Below, there is a list of generic Thing types that are recommended to be
supported by both client applications and device Bindings in Integration packages.
For every generic Thing type, there are device icons, lists of Capabilities
and other parameters recommended to be implemented by Bindings and supported
by client applications. Use the left navigation menu to find any device type
quickly.


Value Sensor
============

:type: "value_sensor"

:inherits from: none

:icon: two random digits or a sensor icon

:capabilities: "has_value"

A generic type of sensors which represent their results of measurements
in numbers of an unspecified unit. Such values must to be displayed
to user in the same manner: "current value is %d", where "%d" is an
placeholder for the measured value. Must to be used rarely, only if
there is no more specific device type declared.


Binary Sensor
=============

:type: "binary_sensor"

:inherits from: "value_sensor"

:icon: "I/O" text or a similar-looking icon

:capabilities: "has_value", "is_active"

The most primitive (but not necessary the base) type of Sensors in the
system. Can have only one of two integer values: 1 and 0. Where 1 is
mapped to the "active" state and 0 is mapped to "not active". Usually
is inherited by more specific implementations of a Binary Sensor,
including buttons, leakage sensors, reed switches (detects an opening
of a door or window), motion sensors and so on.


Button
======

:type: "button"

:inherits from: "binary_sensor"

:icon: an icon of a button

:capabilities: "has_value", "is_active"

Represents all the Buttons connected to the system. Its value is set
to 1 while the button is pressed and sets to 0 just after the button
was released. There is no long press detection, double press detection
and so on. Just "pressed" (1) and released (0). All the other
functionality is the same as in Binary Sensor.


Switch
======

:type: "switch"

:inherits from: "binary_sensor"

:icon: an icon of a switch (or a reed switch)

:capabilities: "has_value", "is_active"

Another kind of a Binary Sensor. Is a base type for devices which can
preserve their state without the help of a user (i.e. user doesn't need
to keep the switch pressed). Physically, it can be a simple light switch,
toggle switch, reed switch and on and on. As any other Binary Sensor,
the "value" field value can be equal to either 1 or 0, where 1 is mapped
to "active" and 0 is mapped to "not active".


Contact Sensor
==============

:type: "contact_sensor"

:inherits from: "switch"

:icon: an icon of a reed switch or an opened door without a handle

:capabilities: "has_value", "is_active", "has_state", "open_closed"

The special subtype of a Switch. Adds a new field to the list: a
"has_state" field which can take either "opened" or "closed" value,
where "opened" is equal to 1 and "closed" is equal to 0.


Motion Sensor
=============

TBD. Has the same logic as Button


Leakage Sensor
==============

TBD. Has the same logic as Switch


Temperature Sensor
==================

:type: "temperature_sensor"

:inherits from: none

:icon: an icon of a thermometer

:capabilities: "has_temperature"

Temperature Sensor represents simple thermometers, temperature sensors
which displays the current temperature of controlled object: in-room
air temperature, outside temperature, temperature of a human body, etc.
If your device implements some features in addition to measuring of
temperature - please, consider some other base types for your device.


Humidity Sensor
===============

TBD. Almost the same as Temperature Sensor but measures humidity
instead of temperature.


Climate Station
===============

TBD. Combines functions of humidity, temperature, gas and air quality
sensors.


Lock
====

:type: "lock"

:inherits from: none

:icon: an icon of a keyhole or padlock

:capabilities: "actuator", "has_state", "is_active", "open_closed"

Represents all kinds of controllable Locks. Allows to at least lock
the controlled door, gate or another object. Unlocking capability is
optional. The "state" field can take either one of the end state
values ("opened" or "closed") or one of the transitional state values
("opening", "closing").


Shades
======

:type: "shades"

:inherits from: none

:icon: an icon of a window with shades

:capabilities: "actuator", "has_state", "is_active", "open_closed"

:optional_capabilities: "has_position"

Represents all kinds of shades - materials which cover the window and
reduces the amount of light passed through it. Also named as sunblinds,
shutters, louvers and so on. Their state can take either "opened" or
"closed" values, where "opened" is equal to "active" and "closed"
equal to "not active". Two transitional states are also possible:
"opening" and "closing". Some shades can also provide an "has_position"
capability that allows to set the position of shades in percents
from 0 to 100, regarding to the area of window covered by shades.


Light
=====

:type: "light"

:inherits from: none

:icon: pendant lamp icon

:capabilities: "actuator", "has_state", "is_active", "on_off"

Light is a common type for all lightning devices: LED strips, light bulbs,
floor lamps and so on. The base functionality of such devices is to be turned
on and off. And to emit a light in the turned on state.


Dimmable Light
==============

:type: "dimmable_light"

:inherits from: "light"

:icon: pendant lamp icon

:capabilities: "actuator", "has_state", "is_active", "on_off", "has_brightness"

Dimmable Light is a common device type for all lighting devices that can be
dimmed, i.e. that can change their level of brightness. The rest of functionality
is inherited from the base Light device type.


Colour Temperature Light
========================

:type: "ct_light"

:inherits from: "dimmable_light"

:icon: pendant lamp icon

:capabilities:
    "actuator", "has_state", "is_active", "on_off", "has_brightness",
    "has_color_temperature"

Color Temperature Light is a common device type for all lighting devices that
can change their color temperature. The rest of functionality is inherited
from the base Dimmable Light device type.


Colour Light
============

:type: "colour_light"

:inherits from: "ct_light"

:icon: colorized pendant lamp icon

:capabilities:
    "actuator", "has_state", "is_active", "on_off", "has_brightness",
    "has_color_temperature", "has_color_hsb"

:optional_capabilities: "has_color_rgb"

Colour Light is a common device type for all lighting devices that can
change their colour of light. The rest of functionality is inherited
from the base Colour Temperature Light device type.

Additionally, devices can support an "has_color_rgb" capability which
allows to set a color in RGB color units. This capability is optional
because not all devices on the market support it. And often it's hard
to determine a clear mapping between RGB and HSB color values.


Power Switch
============

:type: "power_switch"

:inherits from: none

:icon: switch icon

:capabilities:
    "actuator", "has_state", "is_active", "on_off"

Power Switch type represents all power switches in the system. Such
power switches include smart power outlet, circuit breakers, switches
that are not Light switches and other similar devices. The only
functionality of such devices is to turn connected load on and off.

If your power switch or power outlet implements an additional
functionality or is not really a power switch - please, search for
a more appropriate base type in this documentation or
file an issue on GitHub [#f5]_.


Valve
=====

:type: "valve"

:inherits from: none

:icon: valve icon

:capabilities:
    "actuator", "has_state", "is_active", "open_closed"

Valve represents an externally controllable valve for gas, liquid or
other matter which can be either in "opened" or "closed" state.
Transitional states "opening" and "closing" are also possible.

In addition to valve-specific device states and commands, valves
support an "is_active" capability where "active" is equal to
"opened" and "not active" is linked to "closed".


Fan
===

:type: "fan"

:inherits from: none

:icon: fan icon

:capabilities:
    "actuator", "has_state", "is_active", "on_off"

Fans is the most primitive type of the climatic devices. Fans can
be either in "on" or "off" states while fan speed control is not
supported. Additional functionality like enabling and disabling
heaters is not supported too.


Variable Speed Fan
==================

:type: "vs_fan"

:inherits from: "fan"

:icon: fan icon

:capabilities:
    "actuator", "has_state", "is_active", "on_off", "fan_speed"

Variable Speed Fans are fans whose speed of rotation can be controlled.
In the rest, it's just a usual Fan described above.


Player
======

:type: "player"

:inherits from: none

:icon: "play" icon in a circle

:capabilities:
    "actuator", "has_state", "is_active", "play_stop"

:optional capabilities:
    "on_off", "has_volume"

Player is a base type for all kinds of players: audio players, video
players, streaming players, radios and so on and so forth. Such devices
doesn't allow to change tracks, pause the playback or do anything
similar. They can be only in one of two states: "playing" and "stopped",
where "playing" state is mapped to the "active" state while "stopped" to
"not active".

The "on_off" Capability can be provided by real, hardware players. In
such case, it's recommended to provide a separate button to control
player's power and separate buttons to control playback.

Some players can also provide an "has_volume" capability but it's not
absolutely necessary.


Pausable Player
===============

:type: "pausable_player"

:inherits from: "player"

:icon: "play" icon in a circle

:capabilities:
    "actuator", "has_state", "is_active", "play_stop", "pausable"

:optional capabilities:
    "on_off", "has_volume"

Pausable Player type represents all Players which support pausing -
temporarily stopping of playback with saving of the current playback
position. In general, it's the same Player as described above with
all its functions and limitations. The only thing that was added
is an additional "paused" state and a corresponding "pause" command.


Track Player
============

:type: "track_player"

:inherits from: "pausable_player"

:icon: "play" icon in a circle

:capabilities:
    "actuator", "has_state", "is_active", "play_stop", "pausable",
    "track_switching", "track_info"

:optional capabilities:
    "on_off", "has_volume"

Track Player type represents all devices with an ability to switch
between tracks: backward and forward. It inherits all the fields and
behaviour provided by Pausable Player type but adds two additional
commands: "next" and "previous". Also, there is new field "track_info"
added that allows to find general information about the current playing
audio track, video, station or stream.


Playlist Player
===============

TBD. Allows to view and manage playback playlist (or queue).


Positional Player
=================

TBD. Reports the current playback position. Supports track rewinding.


Speaker
=======

:type: "speaker"

:inherits from: none

:icon: speaker icon

:capabilities:
    "actuator", "has_state", "is_active", "on_off", "has_volume"

Speaker is a common device type for all sound speakers with a single
input source. The only thing they can do is to be turned on, off
and regulate their volume (i.e. the level of loudness).

Please not that muted devices and devices with a volume set to zero
are still considered as "active" devices. So, Speakers are considered
to be in "active" state until they are not powered off.


Speaker System
==============

:type: "speaker_system"

:inherits from: "speaker"

:icon: speaker system icon

:capabilities:
    "actuator", "has_state", "is_active", "on_off", "has_volume",
    "multi_source"

Speaker System is a common device type for all sound speakers and
speaker systems that have multiple input sources. In addition to the
base functionality of a Speaker, such devices allow to view, choose and
change the sound source from the list of provided sources.


Sound System
============

TBD. Multi-functional device. Can be either music player or a
multi-source speaker (i.e. Speaker System) depending on a current mode.


Display
=======

TBD. Can be turned on, off and change screen brightness.


Multi-Source Display
====================

TBD. Can change the source of a displayed picture.


TV
==

TBD. Multi-mode device which can be either Player, Streaming Player or
Multi-Source Display, depending on the current mode.


Virtual Remote Control
======================

TBD. A device that just provides a list of available commands, a list
of corresponding virtual buttons and no feedback from the controlled
system.


.. rubric:: Footnotes

.. [#f1] Light bulb *speakers* or light bulb *with* speakers? Sony LSPX-100E26J

.. [#f2] Toasteroid: http://kck.st/2b5uRHy

.. [#f3] Why not to add a display and Bluetooth audio support too?
   https://goo.gl/VRKYp5

.. [#f4] Samsung Family Hub

.. [#f5] All issues can be reported on the project's page:
   https://github.com/s-kostyuk/everpl/issues
