# Include standard modules
import unittest

# Include 3rd-party modules

# Include DPL modules
from dpl.placements import Placement, PlacementBuilder


class TestPlacementBuilder(unittest.TestCase):
    def test_build(self):
        placement_id = "R1"
        placement_name = "Corridor"
        placement_image = "http://www.gesundheittipps.net/wp-content/uploads/2016/02/Flur_547-1024x610.jpg"

        config = {
            "id": placement_id,
            "friendly_name": placement_name,
            "image_url": placement_image
        }

        placement = PlacementBuilder.build(config)  # type: Placement

        self.assertTrue(isinstance(placement, Placement))

        self.assertEqual(placement.placement_id, placement_id)
        self.assertEqual(placement.friendly_name, placement_name)
        self.assertEqual(placement.image_url, placement_image)

    # TODO: Add more tests:
    # - missing params and default values
    # - missing mandatory params


if __name__ == '__main__':
    unittest.main()
