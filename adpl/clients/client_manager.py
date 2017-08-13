# Include standard modules
import asyncio
import logging
from uuid import UUID

# Include 3rd-party modules
# Include DPL modules
from adpl import api
from adpl import clients


class ClientManager(object):
    """
    ClientManager is a class that stores and manages information about all users of
    the system and their client devices
    """
    def __init__(self):
        """
        Constructor without parameters
        """
        self._users = dict()  # type: dict[UUID, clients.User]
        self._clients = dict()  # type: dict[UUID, clients.Client]

    @property
    def users(self) -> dict[UUID, clients.User]:
        """
        A read-only property which returns a collection of users
        :return: a dict with key = UserID and value = an instance of User
        """
        return self._users

    @property
    def clients(self) -> dict[UUID, clients.Client]:
        """
        A read-only property which returns a collection of clients
        :return: a dict with key = ClientID and value = an instance of Client
        """
        return self._clients

    def get_user_by_client(self, client_id: UUID) -> clients.User:
        """
        Find a user by ID of its client
        :return: an instance of clients.User
        """
        raise NotImplementedError

    def add_user(self, user_ins: clients.User) -> UUID:
        """
        Add a user to the system and assign a UUID to him
        :param user_ins: a prepared instance of client.User
        :return: an assigned ID of User
        """
        pass
