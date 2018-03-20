# Include standard modules
import unittest
import uuid

# Include 3rd-party modules

# Include DPL modules
from dpl.model.user import User


class TestUser(unittest.TestCase):
    test_username = 'Foo'
    test_password = 'Bar'

    def setUp(self):
        self.test_uuid = uuid.uuid4()
        self.sample_user = User(
            self.test_uuid,
            self.test_username,
            self.test_password
        )

    def test_user_creation(self):
        sample_user = User(
            self.test_uuid,
            self.test_username,
            self.test_password
        )

        self.assertEqual(sample_user.domain_id, self.test_uuid)
        self.assertEqual(sample_user.username, self.test_username)
        self.assertTrue(sample_user.verify_password(self.test_password))

    def test_user_creation_empty_username(self):
        with self.assertRaises(ValueError):
            User(
                self.test_uuid,
                '',
                self.test_password
            )

    def test_user_update_username(self):
        new_username = 'FooBar'
        self.sample_user.username = new_username

        self.assertEqual(self.sample_user.username, new_username)

    def test_user_update_empty_username(self):
        with self.assertRaises(ValueError):
            self.sample_user.username = ''

    def test_user_update_password(self):
        new_password = 'FooBar'
        self.sample_user.update_password(self.test_password, new_password)

        self.assertTrue(self.sample_user.verify_password(new_password))

    def test_user_update_password_wrong_old_password(self):
        new_password = 'FooBar'

        with self.assertRaises(ValueError):
            self.sample_user.update_password(
                self.test_password + '111',
                new_password
            )


if __name__ == '__main__':
    unittest.main()
