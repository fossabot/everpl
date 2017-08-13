# Include standard modules
import unittest

# Include 3rd-party modules

# Include DPL modules
from adpl.auth.user import User


class TestUser(unittest.TestCase):
    test_username = 'Foo'
    test_password = 'Bar'

    def test_user_creation(self):
        sample_user = User(self.test_username, self.test_password)

        self.assertEqual(sample_user.username, self.test_username)
        self.assertTrue(sample_user.verify_password(self.test_password))

    def test_user_creation_empty_username(self):
        with self.assertRaises(ValueError):
            User('', self.test_password)

    def test_user_update_username(self):
        sample_user = User(self.test_username, self.test_password)

        new_username = 'FooBar'
        sample_user.username = new_username

        self.assertEqual(sample_user.username, new_username)

    def test_user_update_empty_username(self):
        sample_user = User(self.test_username, self.test_password)

        with self.assertRaises(ValueError):
            sample_user.username = ''

    def test_user_update_password(self):
        sample_user = User(self.test_username, self.test_password)

        new_password = 'FooBar'
        sample_user.update_password(self.test_password, new_password)

        self.assertTrue(sample_user.verify_password(new_password))

    def test_user_update_password_wrong_old_password(self):
        sample_user = User(self.test_username, self.test_password)

        new_password = 'FooBar'

        with self.assertRaises(ValueError):
            sample_user.update_password(self.test_password + '111', new_password)


if __name__ == '__main__':
    unittest.main()
