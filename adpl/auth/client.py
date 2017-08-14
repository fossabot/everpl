class Client(object):
    """
    Client is a class that stores information about a registered client device
    """
    def __init__(self):
        raise NotImplementedError

    # FIXME: CC3: Store only a hash of access token and add verify_token method?
    def token(self) -> str:
        """
        Return an access token which is associated with this client
        :return: access token, a string
        """
        raise NotImplementedError

    def refresh_token(self) -> str:
        """
        Invalidates current access token and returns a new one
        :return: a new access token, a string
        """
        raise NotImplementedError

    # FIXME: Specify a type of return value
    @property
    def client_type(self):
        """
        A type of client device or application like Web, Android, iPhone, CLI application and so on
        :return: type information
        """
        raise NotImplementedError

    @property
    def metadata(self) -> dict:
        """
        Additional type-specific metadata about this client
        :return: a dict of data
        """
        raise NotImplementedError

