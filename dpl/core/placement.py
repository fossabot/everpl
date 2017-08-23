class Placement(object):
    """
    Placement is an entity class that stores information about a specific placement (position)
    of Thing. For example, in Smart Home systems, each Placement can represent one
    room at the house and contain information about a name of the room, its internal
    identifier and an image of this room.
    """
    def __init__(self, placement_id: str, friendly_name: str = None, image_url: str = None):
        """
        Constructor
        :param placement_id: some unique identifier of this entity
        :param friendly_name: human-friendly name of this placement
        :param image_url: an URL to the illustration image
        """
        # TODO: Add params validation here
        self._placement_id = placement_id
        self._friendly_name = friendly_name
        self._image_url = image_url

    @property
    def placement_id(self) -> str:
        """
        Contains an unique identifier of this entity. Can't be changed after init.
        :return: string, system-internal identifier
        """
        return self._placement_id

    @property
    def friendly_name(self) -> str:
        """
        Contains some short meaningful human-readable naming of this placement
        :return: string, placement's name
        """
        return self._friendly_name

    @friendly_name.setter
    def friendly_name(self, new_value: str):
        """
        A setter for friendly_name property
        :param new_value: new value of name to be set
        :return: None
        """
        # TODO: Add value validation here
        self._friendly_name = new_value

    @property
    def image_url(self) -> str:
        """
        Stores an URL to the illustration image for this placement
        :return: string representation of URL
        """
        return self._image_url

    @image_url.setter
    def image_url(self, new_value: str):
        """
        A setter for image_url property
        :param new_value: new value to be set
        :return: None
        """
        # TODO: Add value validation here
        self._image_url = new_value
