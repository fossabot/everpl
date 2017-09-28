# Include standard modules
from typing import Dict

# Include 3rd-party modules
# Include DPL modules
from .placement import Placement


class PlacementBuilder(object):
    """
    PlacementBuilder is a class with the only one method available:
    "build".
    """
    @staticmethod
    def build(config: Dict) -> Placement:
        """
        Build method just creates an instance of Placement
        based on the specified configuration params.

        :param config: configuration params
        :return: a constructed instance of Placement
        """
        new_placement = Placement(
            placement_id=config["id"],
            friendly_name=config["friendly_name"],
            image_url=config["image_url"]
        )

        return new_placement
