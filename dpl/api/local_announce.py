"""
This module contains an implementation of everpl announcement logic for
local networks
"""

import socket

import zeroconf


class LocalAnnounce(object):
    """
    This class controls the announcement of everpl instance presence in the
    local network using Zeroconf (Avahi / Bonjour) protocol
    """
    _service_type = "_everpl._tcp.local."

    def __init__(self):
        """
        Initializes Zeroconf instance and starts corresponding threads
        """
        self._zeroconf = zeroconf.Zeroconf()

    def create_server(
            self, instance_name: str = None,
            address: str = "127.0.0.1", port: str = 10800,
            server_host: str = None
    ) -> None:
        """
        Initializes zeroconf service (everpl hub) announcement with the
        specified optional params

        :param instance_name: the name of this service (instance, hub);
               set to the "everpl hub @ hostname._everpl.tcp" by default
        :param address: an IP address of this instance; set to the 127.0.0.1
               by default
        :param port: the port of announced service; set to the 10800 by default
        :param server_host: hostname of this instance; set to the
               "hostname.local" local
        :return: None
        """
        hostname = socket.gethostname()

        if instance_name is None:
            instance_name = "everpl hub @ %s.%s" % (
                hostname, self._service_type
            )

        coded_address = socket.inet_aton(address)

        if server_host is None:
            server_host = "%s.local" % hostname

        txt_properties = {}

        service_info = zeroconf.ServiceInfo(
            type_=self._service_type,
            name=instance_name,
            address=coded_address,
            port=port,
            properties=txt_properties,
            server=server_host
        )

        self._zeroconf.register_service(service_info)

    def shutdown_server(self) -> None:
        """
        Unregisters everpl zeroconf service. Stops announcement of this hub

        :return: None
        """
        self._zeroconf.unregister_all_services()
        self._zeroconf.close()
