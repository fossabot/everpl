from dpl.model.base_entity import BaseEntity


class Connection(BaseEntity):
    """
    Connection is a class that abstracts the details of specific
    protocol and way of communication with specific devices.
    One connection can be used by different devices (thing).
    """
    pass
