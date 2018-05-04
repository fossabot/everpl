Local network discovery
=======================

General information
-------------------

Starting from v0.3 of the platform all everpl instances (everpl hubs)
are able to be discovered in a local network by default.

Hubs announce their presence and can be discovered using a Zeroconf
(Avahi/Bonjour) protocol - Zero Configuration Networking protocol.
This protocol allows services to announce their presence in the system,
to assign constant domain names in a ".local" domain zone, to resolve
such domain names and to look for a specific service in the system.

For more information about Zeroconf you can read an article on Medium
titled `"Bonjour Android, it’s Zeroconf"`_. It tells about Zeroconf
protocols in general, about Bonjour/Avahi approach and how it relates
with client applications and service discovery.

.. _`"Bonjour Android, it’s Zeroconf"`:
   https://medium.com/@_tiwiz/bonjour-android-its-zeroconf-8e3d3fde760e

Unfortunately, Zeroconf (and UDP multicast in general) isn't supported
by modern web browsers.

For more detailed information see:

- DNS-SD protocol website: `<http://www.dns-sd.org/>`_, covers service
  discovery part of functionality;
- mDNS protocol website: `<http://www.multicastdns.org/>`_, covers
  domain name association in ".local" domain zone;
- and corresponding RFCs.

For testing purposes you can use such handy tools as:

- Avahi-Discover GUI utility for Linux:
  https://linux.die.net/man/1/avahi-discover
- Service browser for Android:
  https://play.google.com/store/apps/details?id=com.druk.servicebrowser&hl=en_US
- dns-sd CLI tool for macOS

How to discover an everpl hub
-----------------------------

In order to discover an everpl hub you need to use one of the Zeroconf
libraries (like build-in NSD for Android) and search for a service type
``_everpl._tcp``. By default such devices will have a name defined as
"everpl hub @ hostname". To access an everpl REST API on a device you
can use name and port, defined in Hostname (Server) and Port fields of
a discovery response correspondingly.

Here is an example of a complete discovery response (as displayed by
console avahi-browse utility):

::

    = virbr0 IPv4 everpl hub @ hostname_was_here              _everpl._tcp         local
       hostname = [hostname_was_here.local]
       address = [192.168.20.1]
       port = [10800]
       txt = []
