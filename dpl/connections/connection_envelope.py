# Include standard modules
from typing import Any

# Include 3rd-party modules

# Include DPL modules
from dpl.connections.connection import Connection


class ConnectionEnvelope(Connection):
    """
    ConnectionEnvelope is created for cases when you don't want to implement
    specific connection by yourself or modify its public interface in some way.

    In this case you can place an existing protocol implementation class into
    ConnectionEnvelope and use it directly from your implementation of Thing.
    """
    def __init__(self, underlying_connection: Any):
        """
        A constructor
        :param underlying_connection: an instance of existing connection implementation
        """
        self._content = underlying_connection

    @property
    def content(self) -> Any:
        """
        Returns a saved instance of underlying connection
        :return:
        """
        return self._content
