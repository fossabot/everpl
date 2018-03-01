Capabilities
============

As was known, different devices implement the different functionality.
Some devices report current climate conditions like humidity,
temperature and atmospheric pressure. Other devices are able to change
such conditions in your home like air conditioners, humidifiers and
climate systems. Other devices allows to play music, videos, display
photos and so on.

In everpl such pieces of functionality which are implemented by specific
devices (Things) are called Capabilities.

Each Capability is some abstract atomic piece of functionality which can
be implemented or provided by some device (Thing). Each Capabilities
can provide some new properties (fields, data) of a Thing and/or commands
that can be send to device for execution.

One device can have several different Capabilities. For example, there
already mentioned climatic devices which are capable of measuring
temperature, relative humidity and, maybe, CO2 levels. There are RGB
which can be turned on and off, change their brightness and even change
their color. There are Smart-TVs which is capable of doing... a lot of
stuff.

In general, different Capabilities can be mixed in arbitrary combinations.
In REST API and internal representation of the Thing the list of supported
capabilities is specified in ``capabilities`` property of a Thing.

The list of all Capabilities that can be provided by a Thing, the list of
properties and commands they provide is specified on the
:ref:`next page <possible_capabilities>`.
