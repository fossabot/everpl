# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from . import Connection


class ConnectionFactory(object):
    """
    ConnectionFactory is a class that have only one method called 'build'
    that builds an instance of connection by specified configuration.
    """
    @staticmethod
    def build(*args, **kwargs) -> Connection:
        """
        Build: create a specific instance of connection by specified params
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: an instance of Connection
        """
        raise NotImplementedError
