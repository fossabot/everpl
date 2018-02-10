import os
import binascii


def generate_token(length: int = 40) -> str:
    """
    Generates a random token with a specified length

    :return: bytes-encoded string
    """
    n_of_bytes = length // 2

    return os.urandom(n_of_bytes).hex()

