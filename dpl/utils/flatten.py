import itertools
import typing


def flatten(collection: typing.Iterable) -> typing.Iterable:
    """
    Flattens a collection of iterables, i.e. converts
    (("one",), ("two", ), ("three"),)
    into
    ("one", "two", "three")

    :param collection: a collection to be flattened
    :return: an sequence that represents the results of flattering
    """
    return itertools.chain.from_iterable(collection)
