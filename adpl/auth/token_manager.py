# Include standard modules
from typing import Dict, List
import binascii
import os

# Include 3rd-party modules

# Include DPL modules
from adpl.auth.user import User
from adpl.utils import generate_token


class TokenManager(object):
    """
    TokenManager is a class that is responsible for generating of new tokens,
    their revocation and for determining of User (or Client) which is
    associated with this token
    """
    def __init__(self):
        self.__tokens = dict()  # type: Dict[str, User]

    # FIXME: CC6: Change token type from str to bytes?
    def generate_token(self, token_owner) -> str:
        """
        Generates a new token for some User (or Client)
        :param token_owner: User or Client which is associated with token
        :return: a new token
        """
        # TODO: Ensure that the user is present in the system at all

        new_token = generate_token().decode(encoding='utf-8')

        assert new_token not in self.__tokens

        self.__tokens[new_token] = token_owner

        return new_token

    def remove_token(self, token: str):
        """
        Revoke generated token
        :param token: a token to be revoked
        :return: None
        """
        if token not in self.__tokens:
            raise ValueError("No such token registered")

        self.__tokens.pop(token)

    def remove_all_tokens(self, token_owner):
        """
        Revoke all generated tokens for specific User or Client
        :param token_owner: User or Client which is associated with tokens to be revoked
        :return: None
        """
        on_removal = list()  # type: List[str]

        # Get a full list of tokens which are related to specific owner
        # (collection can't be mutated during iteration)
        for key, value in self.__tokens.items():
            if value == token_owner:
                on_removal.append(key)

        # FIXME: CC5: Remove this check and ignore an absence?
        if not on_removal:  # if there are no tokens registered with a specified owner
            raise ValueError("Specified owner doesn't own any tokens")

        # Remove each pending token
        for key in on_removal:
            self.__tokens.pop(key)

    def resolve_token_owner(self, token: str):
        """
        Determine an owner of specified token
        :param token: token to be resolved
        :return: an object of User or Client that owns the token
        """
        return self.__tokens[token]

    def is_token_present(self, token: str) -> bool:
        """
        Checks if the specified token is registered in the system
        :param token: token to be checked
        :return: true if token is registered, false otherwise
        """
        return token in self.__tokens
