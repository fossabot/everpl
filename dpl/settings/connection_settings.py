from typing import Any, Mapping
from types import MappingProxyType

from dpl.model.base_entity import BaseEntity
from dpl.model.domain_id import TDomainId


class ConnectionSettings(BaseEntity):
    """
    ConnectionSettings is a some entity which is responsible
    for storage of all data needed to initialize a Connection
    like its unique identifier, an identifier of Integration
    which provides this type of Connections, a type of this
    Connection provided by Integration and some additional
    implementation-specific connection parameters
    """
    def __init__(
            self, domain_id: TDomainId, integration: str,
            con_type: str, con_params: Mapping[str, Any]
    ):
        """
        Constructor. Receives all data needed to store in
        an instance of ConnectionSettings

        :param domain_id: a unique identifier of connection
               to be configured
        :param integration: a name of the Integration which
               provides implementation of this Connection
        :param con_type: an Integration-specific type
               identifier of this Connection
        :param con_params: some implementation-specific
               parameters to be used for Connection configuration
        """

        super().__init__(domain_id)

        self._integration = integration
        self._con_type = con_type
        self._con_params = con_params

    @property
    def integration(self) -> str:
        """
        Returns a name of the Integration which provides
        implementation of this Connection

        :return: a name of the Integration which provides
                 implementation of this Connection
        """
        return self._integration

    @property
    def connection_type(self) -> str:
        """
        Returns an Integration-specific type identifier
        of this Connection

        :return: an Integration-specific type identifier
                 of this Connection
        """
        return self._con_type

    @property
    def connection_params(self) -> Mapping[str, Any]:
        """
        Returns some implementation-specific parameters
        to be used for Connection configuration in a form
        a read-only dictionary

        :return: some implementation-specific parameters
                 to be used for Connection configuration
        """
        return MappingProxyType(self._con_params)
