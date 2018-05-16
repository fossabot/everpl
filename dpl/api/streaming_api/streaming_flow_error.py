"""
This module contains description of a single exception to be raised if
something wrong had happened in Streaming API communication flow
"""


from typing import Mapping


class StreamingFlowError(Exception):
    """
    This exception can be raised if something wrong will happen in
    Streaming API communication flow. Contains information about an error to
    be passed to client
    """
    def __init__(self, error_info: Mapping):
        """
        Constructor. Saves information about the happened error

        :param error_info: information about the happened error
        """
        self.error_info = error_info
