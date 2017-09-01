# Include standard modules
from typing import Any
import io

# Include 3rd-party modules
# Include DPL modules
from dpl.connections import Connection
from dpl.platforms import ConnectionFactory, ConnectionRegistry


class DummyConnection(Connection):
    """
    A dummy connection class that allows just to print some data to console
    or some other file (stream) with a specified prefix.
    """
    def __init__(self, file: io.TextIOBase = None):
        """
        Constructor receives a file or file-like object that will be used for printing.
        sys.stdout will be used by default

        :param file: file-like object (stream) that will be used for printing
        """
        self._file = file

    def print(self, prefix: str, data: Any) -> None:
        """
        Print some data to file/console with a specified prefix

        :param data: data to be printed
        :param prefix: prefix to be printed before the specified data
        :return: None
        """
        print(prefix + data, file=self._file)


class DummyConnectionFactory(ConnectionFactory):
    """
    DummyConnectionFactory is a class that is responsible for building of DummyConnections
    """
    @staticmethod
    def build(*args, **kwargs) -> DummyConnection:
        return DummyConnection(*args, **kwargs)


ConnectionRegistry.register_factory(
    connection_type="dummy_connection",
    factory=DummyConnectionFactory()
)
