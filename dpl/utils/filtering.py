from typing import List, Dict


def is_correct_filter(filter_fields, filter_pattern: dict = None):
    """
    Checks if all keys of filter_pattern are present in a set of filter_fields

    :param filter_fields: a set of fields names for which filtering is allowed
    :param filter_pattern: a dictionary used for filtering with keys = field names
           and values = desired values of fields itself
    :return: True if all keys of filter_pattern are present in a set of filter_fields,
             False otherwise.
    """
    for item in filter_pattern.keys():
        if item not in filter_fields:
            return False

    return True


def is_matches(obj: dict, filter_pattern: dict) -> bool:
    """
    Checks if all values of fields in the filter_pattern are the
    same as the corresponding values in 'obj' dictionary

    For example:
    >>> pattern = {"placement": "R1"}
    >>> obj = {"id": 1, "placement": "R1"}
    >>> is_matches(obj, pattern)
    True
    >>> is_matches(obj, {})
    True
    >>> new_pattern = {"nonexistent": "value"}
    >>> is_matches(obj, new_pattern)
    False

    :param obj: a dictionary representation of some object
    :param filter_pattern: a pattern for filtering
    :return: True if all keys (field names) from filter_pattern
             are also present in obj dictionary AND those keys
             have the same values. Returns False otherwise.
    """
    for key, value in filter_pattern.items():
        if obj.get(key, None) != value:
            return False

    return True


def filter_items(items: List[Dict], filter_pattern: dict) -> List[Dict]:
    """
    Performs a simple filtering of data. Returns a subset of items which have
    their values equal to the corresponding values in filter_pattern.

    For example:
    >>> test_values = [{"id": 1, "placement": "R1"}, {"id": 2, "placement": "R2"}]
    >>> filter_pattern = {"placement": "R1"}
    >>> filter_items(test_values, filter_pattern)
    [{'placement': 'R1', 'id': 1}]

    :param items: a list of dict-like representations of some objects
    :param filter_pattern: a dictionary of field names and their desired values
    :return: a list of thing representations which have values corresponding to filtering params
    """
    result = [i for i in items if is_matches(i, filter_pattern)]

    return result
