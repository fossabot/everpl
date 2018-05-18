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
because not all devices on the market support it. And ofter it's hard
to determine a clear mapping between RGB and HSB color values.



.. rubric:: Footnotes

.. [#f1] Light bulb *speakers* or light bulb *with* speakers? Sony LSPX-100E26J

.. [#f2] Toasteroid: http://kck.st/2b5uRHy

.. [#f3] Why not to add a display and Bluetooth audio support too?
   https://goo.gl/VRKYp5

.. [#f4] Samsung Family Hub
