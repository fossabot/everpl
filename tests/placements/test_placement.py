# Include standard modules
import unittest

# Include 3rd-party modules
# Include DPL modules
from dpl.placements import Placement


class TestPlacement(unittest.TestCase):
    test_id = "R1"
    test_friendly_name = "Bathroom"
    test_image_url = "https://c1.staticflickr.com/3/2310/5788748100_61268372cc_b.jpg"

    def test_default_construction(self):
        placement = Placement(
            self.test_id
        )

        self.assertEqual(placement.domain_id, self.test_id)
        self.assertEqual(placement.friendly_name, None)
        self.assertEqual(placement.image_url, None)

        self.assertTrue(isinstance(placement.domain_id, str))

    def test_params_constructor(self):
        placement = Placement(
            self.test_id,
            self.test_friendly_name,
            self.test_image_url
        )

        self.assertEqual(placement.domain_id, self.test_id)
        self.assertEqual(placement.friendly_name, self.test_friendly_name)
        self.assertEqual(placement.image_url, self.test_image_url)

    def test_id_unchangeable(self):
        placement = Placement(
            self.test_id,
            self.test_friendly_name,
            self.test_image_url
        )

        with self.assertRaises(AttributeError):
            placement.domain_id = self.test_id + "_1"

    def test_id_friendly_name_setter(self):
        placement = Placement(
            self.test_id,
            self.test_friendly_name,
            self.test_image_url
        )

        new_name = "Bedroom"
        assert self.test_friendly_name != new_name

        placement.friendly_name = new_name
        self.assertEqual(placement.friendly_name, new_name)

    def test_id_image_url_setter(self):
        placement = Placement(
            self.test_id,
            self.test_friendly_name,
            self.test_image_url
        )

        new_image = "https://cdn.pixabay.com/photo/2015/08/09/00/31/bedroom-881123_960_720.jpg"
        assert self.test_image_url != new_image

        placement.image_url = new_image
        self.assertEqual(placement.image_url, new_image)

if __name__ == '__main__':
    unittest.main()
