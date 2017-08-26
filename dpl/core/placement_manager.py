# Include standard modules
from typing import List, Dict, ValuesView

# Include 3rd-party modules
# Include DPL modules
from .placement import Placement


class PlacementManager(object):
    """
    PlacementManager is a class that is responsible for initialization, storage
    and fetching of placements.
    """
    def __init__(self):
        """
        Default constructor
        """
        self._placements = dict()  # type: Dict[str, Placement]

    def init_placements(self, config: List[Dict]) -> None:
        """
        Init all placements by a specified configuration data
        :param config: configuration data that will be used for building of Placements
        :return: None
        """
        for conf_item in config:
            placement_id = conf_item["id"]
            new_placement = Placement(
                placement_id=placement_id,
                friendly_name=conf_item["friendly_name"],
                image_url=conf_item["image_url"]
            )
            self._placements[placement_id] = new_placement

    def fetch_all_placements(self) -> ValuesView[Placement]:
        """
        Fetch a set-like collection of all stored Placements
        :return: a set-like collection of Placements
        """
        return self._placements.values()

    def fetch_placement(self, placement_id: str, default=None) -> Placement:
        """
        Find specific placement by id
        :param placement_id: an ID of placement to be fetched
        :param default: default value to be returned if the specified placement is not found
        :return: an instance of Placement with the corresponding ID or default value
        """
        return self._placements.get(placement_id, default)
