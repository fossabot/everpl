# Include standard modules
from typing import Dict, Any

# Include 3rd-party modules
# Include DPL modules


def obj_to_dict(o: object) -> Dict[str, Any]:
    """
    Serialize any python object to dictionary. It walks across all public properties
    of an object and saves their values into dictionary
    :param o: an object to be serialized
    :return: a dictionary where keys = property names and values = property values
    """
    result = dict()  # type: Dict[str, Any]

    for attr_name in dir(o):
        # print(attr_name, type(getattr(o, attr_name)))

        if attr_name.startswith('_'):
            # Ignore private attributes
            continue

        attr = getattr(o, attr_name)

        if not callable(attr):
            result[attr_name] = attr

    return result
