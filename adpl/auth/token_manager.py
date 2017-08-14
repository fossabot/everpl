class TokenManager(object):
    """
    TokenManager is a class that is responsible for generating of new tokens,
    their revocation and for determining of User (or Client) which is
    associated with this token
    """
    def __init__(self):
        raise NotImplementedError

    def generate_token(self, token_owner) -> str:
        """
        Generates a new token for some User (or Client)
        :param token_owner: User or Client which is associated with token
        :return: a new token
        """
        raise NotImplementedError

    def remove_token(self, token: str):
        """
        Revoke generated token
        :param token: a token to be revoked
        :return: None
        """
        raise NotImplementedError

    def remove_all_tokens(self, token_owner):
        """
        Revoke all generated tokens for specific User or Client
        :param token_owner: User or Client which is associated with tokens to be revoked
        :return: None
        """
        raise NotImplementedError

    def resolve_token_owner(self, token: str):
        """
        Determine an owner of specified token
        :param token: token to be resolved
        :return: an object of User or Client that owns the token
        """
        raise NotImplementedError
