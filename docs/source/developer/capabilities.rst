Capabilities
============

As known, different devices implement different functionality.
Some devices report current climate conditions like humidity,
temperature and atmospheric pressure. Other devices like air
conditioners, humidifiers and climate systems are able to change
such conditions in the building. Other devices allow to play music,
videos, display photos and so on.

In everpl such pieces of functionality which are implemented by specific
devices (Things) are called Capabilities.

Each Capability is an abstract atomic piece of functionality which can
be implemented or provided by some device (Thing). Each Capability
can define some new properties (fields, data) of a Thing and/or commands
that can be send to device for execution.

One device can have several different Capabilities. For example, there
are already mentioned climatic devices which are capable of measuring
temperature, relative humidity and, maybe, CO2 levels. There are RGB Lamps
which can be turned on and off, change their brightness and even change
their color. There are Smart-TVs which is capable of doing... a lot of
stuff.

In general, different Capabilities can be mixed in arbitrary combinations.
In REST API and internal representation of the Thing the list of supported
capabilities is specified in ``capabilities`` property of a Thing.

The list of all Capabilities that can be provided by a Thing, the list of
properties and commands they provide is specified on the
:ref:`next page <possible_capabilities>`.
