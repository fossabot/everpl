# Include standard modules
import asyncio
import logging
from uuid import UUID
from typing import Dict

# Include 3rd-party modules
# Include DPL modules
from adpl import api
from adpl import auth


class ClientManager(object):
    """
    ClientManager is a class that stores and manages information about all users of
    the system and their client devices
    """
    def __init__(self):
        """
        Constructor without parameters
        """
        self._users = dict()  # type: Dict[UUID, auth.User]
        self._clients = dict()  # type: Dict[UUID, auth.Client]

    @property
    def users(self) -> Dict[UUID, auth.User]:
        """
        A read-only property which returns a collection of users
        :return: a dict with key = UserID and value = an instance of User
        """
        return self._users

    @property
    def clients(self) -> Dict[UUID, auth.Client]:
        """
        A read-only property which returns a collection of auth
        :return: a dict with key = ClientID and value = an instance of Client
        """
        return self._clients

    def get_user_by_client(self, client_id: UUID) -> auth.User:
        """
        Find a user by ID of its client
        :return: an instance of auth.User
        """
        raise NotImplementedError

    def add_user(self, user_ins: auth.User) -> UUID:
        """
        Add a user to the system and assign a UUID to him
        :param user_ins: a prepared instance of client.User
        :return: an assigned ID of User
        """
        pass
