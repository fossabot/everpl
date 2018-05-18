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
