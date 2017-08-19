# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from . import ConnectionFactory


class ConnectionRegistry(object):
    """
    ConnectionRegistry is a class that registers all connections, implemented
    in specific platforms (dpl.platforms module), and returns a corresponding
    ConnectionFactory for building of instance of this connection.
    """
    __registry = dict()  # contains references to all factories

    @classmethod
    def register_factory(cls, connection_type: str, factory: ConnectionFactory) -> None:
        # FIXME: CC10: Add additional platform argument?
        """
        Register a factory for building of instance of corresponding connection type
        :param connection_type: a name of connection type, for which connection factory
            is registered.
        :param factory: an instance of connection factory that will be used for building
            of those type of connections.
        :return: None
        """
        cls.__registry[connection_type] = factory

    @classmethod
    def resolve_factory(cls, connection_type: str, default: ConnectionFactory = None) -> ConnectionFactory:
        """
        Returns an instance of ConnectionFactory that must be used for building of
        specified type of connections.
        :param connection_type: a type of connection that ConnectionFactory is responsible for.
        :param default: object to be returned if related ConnectionFactory is not found
        :return: an instance of ConnectionFactory or None if it's not found
        """
        return cls.__registry.get(connection_type, default)

    @classmethod
    def remove_factory(cls, connection_type: str) -> None:
        """
        Removes an instance of connection factory, that is associated with specified connection type
        :param connection_type: a type of connection that ConnectionFactory was responsible for
        :return: None
        """
        cls.__registry.pop(connection_type)
