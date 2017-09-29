import unittest
import json

from dpl.api.api_errors import ApiError, DOC_BASE_URL


class TestApiErrors(unittest.TestCase):
    ERROR_ID = 1000
    ERROR_DEVEL_MESSAGE = "Unsupported content-type"
    ERROR_USER_MESSAGE = "Invalid request content-type"

    def test_construction(self):
        er = ApiError(self.ERROR_ID)

        self.assertEqual(er.error_id, self.ERROR_ID)
        self.assertEqual(er.docs_url, DOC_BASE_URL + str(self.ERROR_ID))
        self.assertEqual(er.user_message, None)
        self.assertEqual(er.devel_message, None)

    def test_construction_default_user_message(self):
        er = ApiError(self.ERROR_ID, self.ERROR_DEVEL_MESSAGE)

        self.assertEqual(er.user_message, er.devel_message)
        self.assertEqual(er.devel_message, self.ERROR_DEVEL_MESSAGE)

    def test_json_conversion(self):
        er = ApiError(self.ERROR_ID, self.ERROR_DEVEL_MESSAGE, self.ERROR_USER_MESSAGE)

        er_json = json.dumps(er.to_dict())

        er_reconstructed = json.loads(er_json)

        self.assertEqual(er_reconstructed["error_id"], self.ERROR_ID)
        self.assertEqual(er_reconstructed["user_message"], self.ERROR_USER_MESSAGE)
        self.assertEqual(er_reconstructed["devel_message"], self.ERROR_DEVEL_MESSAGE)
        self.assertEqual(er_reconstructed["docs_url"], DOC_BASE_URL + str(self.ERROR_ID))


if __name__ == '__main__':
    unittest.main()
