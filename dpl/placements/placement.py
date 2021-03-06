from typing import Optional

from dpl.model.base_entity import BaseEntity


class Placement(BaseEntity):
    """
    Placement is an entity class that stores information about a specific placement (position)
    of Thing. For example, in Smart Home systems, each Placement can represent one
    room at the house and contain information about a name of the room, its internal
    identifier and an image of this room.
    """
    def __init__(self, domain_id: str, friendly_name: str = None, image_url: str = None):
        """
        Constructor

        :param domain_id: some unique identifier of this entity
        :param friendly_name: human-friendly name of this placement
        :param image_url: an URL to the illustration image
        """
        # TODO: Add params validation here
        # FIXME: CC30: Consider to make friendly_name a non-nullable property
        super().__init__(domain_id)
        self._friendly_name = friendly_name
        self._image_url = image_url

    @property
    def friendly_name(self) -> Optional[str]:
        """
        Contains some short meaningful human-readable naming of this placement

        :return: string, placement's name
        """
        return self._friendly_name

    @friendly_name.setter
    def friendly_name(self, new_value: Optional[str]):
        """
        A setter for friendly_name property

        :param new_value: new value of name to be set
        :return: None
        """
        # TODO: Add value validation here
        self._friendly_name = new_value

    @property
    def image_url(self) -> Optional[str]:
        """
        Stores an URL to the illustration image for this placement

        :return: string representation of URL
        """
        return self._image_url

    @image_url.setter
    def image_url(self, new_value: Optional[str]):
        """
        A setter for image_url property

        :param new_value: new value to be set
        :return: None
        """
        # TODO: Add value validation here
        self._image_url = new_value
