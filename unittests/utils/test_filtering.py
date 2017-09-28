# Include standard modules
import unittest

# Include 3rd-party modules
# Include DPL modules
from dpl.utils import filtering


class TestIsCorrectFilter(unittest.TestCase):
    TEST_DATA = {
        "id": 1,
        "placement": "R1",
        "type": "lighting"
    }

    def test_one_field_name_match(self):
        pattern = {"placement": "R2"}
        self.assertTrue(filtering.is_correct_filter(self.TEST_DATA, pattern))

    def test_two_field_names_match(self):
        pattern = {"placement": "R2", "type": "something"}
        self.assertTrue(filtering.is_correct_filter(self.TEST_DATA, pattern))

    def test_field_name_mismatch(self):
        bad_field_name = "non_existing_field"
        assert bad_field_name not in self.TEST_DATA.keys()

        pattern = {bad_field_name: "R2", "type": "something"}
        self.assertFalse(filtering.is_correct_filter(self.TEST_DATA, pattern))

    def test_empty_pattern_dict_correct(self):
        empty_pattern = {}
        self.assertTrue(filtering.is_correct_filter(self.TEST_DATA, empty_pattern))


class TestIsMatching(unittest.TestCase):
    TEST_DATA = {
        "id": 1,
        "placement": "R1",
        "type": "lighting"
    }

    def test_one_field_match(self):
        pattern = {"placement": "R1"}
        self.assertTrue(filtering.is_matches(self.TEST_DATA, pattern))

    def test_two_fields_match(self):
        pattern = {"placement": "R1", "type": "lighting"}
        self.assertTrue(filtering.is_matches(self.TEST_DATA, pattern))

    def test_first_field_mismatch(self):
        pattern = {"placement": "R1000", "type": "lighting"}
        self.assertFalse(filtering.is_matches(self.TEST_DATA, pattern))

    def test_second_field_mismatch(self):
        pattern = {"placement": "R1000", "type": "hey-ho!"}
        self.assertFalse(filtering.is_matches(self.TEST_DATA, pattern))

    def test_empty_pattern_dict_match(self):
        empty_pattern = {}
        self.assertTrue(filtering.is_matches(self.TEST_DATA, empty_pattern))


class TestFilterItems(unittest.TestCase):
    TEST_DATA = [
        {
            "id": 1,
            "placement": "R1",
            "type": "lighting"
        },
        {
            "id": 2,
            "placement": "R2",
            "type": "player"
        },
        {
            "id": 3,
            "placement": "R4",
            "type": "lighting"
        },
        {
            "id": 4,
            "placement": "R1",
            "type": "player"
        }
    ]

    def test_empty_pattern_match(self):
        pattern = {}
        self.assertEqual(
            filtering.filter_items(self.TEST_DATA, pattern),
            self.TEST_DATA
        )

    def test_select_lighting(self):
        pattern = {"type": "lighting"}

        result = filtering.filter_items(self.TEST_DATA, pattern)

        self.assertEqual(len(result), 2)

        self.assertIn(self.TEST_DATA[0], result)
        self.assertIn(self.TEST_DATA[2], result)

    def test_select_by_r1(self):
        pattern = {"placement": "R1"}

        result = filtering.filter_items(self.TEST_DATA, pattern)

        self.assertEqual(len(result), 2)

        self.assertIn(self.TEST_DATA[0], result)
        self.assertIn(self.TEST_DATA[3], result)

    def test_select_lighting_at_r1(self):
        pattern = {"placement": "R1", "type": "lighting"}

        result = filtering.filter_items(self.TEST_DATA, pattern)

        self.assertEqual(len(result), 1)

        self.assertIn(self.TEST_DATA[0], result)

    def test_select_field_name_mismatch(self):
        pattern = {"something_new": "R1"}

        result = filtering.filter_items(self.TEST_DATA, pattern)

        self.assertTrue(len(result) == 0)

    def test_select_field_value_mismatch(self):
        pattern = {"placement": "R100000"}

        result = filtering.filter_items(self.TEST_DATA, pattern)

        self.assertTrue(len(result) == 0)

if __name__ == '__main__':
    unittest.main()
