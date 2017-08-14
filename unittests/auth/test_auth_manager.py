# Include standard modules
import unittest
from typing import Tuple

# Include 3rd-party modules

# Include DPL modules
from adpl.auth import User
from adpl.auth import AuthManager


class TestAuthManager(unittest.TestCase):
    root_username = 'admin'
    root_password = 'real admin'

    sample_user_name = 'user'
    sample_user_password = 'qwerty'  # Because why not? :)  # Only for testing, of course

    sample_user_2_name = sample_user_name + '2'

    def _get_auth_manager_with_root(self) -> AuthManager:
        am = AuthManager()

        am.create_root_user(
            self.root_username,
            self.root_password
        )

        return am

    def _get_auth_manager_with_sample_user(self) -> Tuple[AuthManager, str]:
        am = self._get_auth_manager_with_root()

        root_token = am.auth_user(
            self.root_username,
            self.root_password
        )

        am.create_user(
            token=root_token,
            username=self.sample_user_name,
            password=self.sample_user_password
        )

        return am, root_token

    def test_creation(self):
        am = AuthManager()

        self.assertFalse(am.users)  # Assert that there is no users after creation

    def test_root_user_creation(self):
        am = AuthManager()

        am.create_root_user(
            self.root_username,
            self.root_password
        )

        self.assertTrue(self.root_username in am.users)

    def test_root_user_creation_twice(self):
        am = AuthManager()

        am.create_root_user(
            self.root_username,
            self.root_password
        )

        with self.assertRaises(ValueError):
            am.create_root_user(
                self.root_username + '_bar',
                self.root_password
            )

    def test_root_user_auth(self):
        am = self._get_auth_manager_with_root()

        token = am.auth_user(
            self.root_username,
            self.root_password
        )

        print(type(token))

        self.assertTrue(isinstance(token, str))

        # TODO: Implement permission checking
        self.assertTrue(am.is_token_grants(token, None))

    def test_root_user_auth_wrong_password(self):
        am = self._get_auth_manager_with_root()

        with self.assertRaises(ValueError):
            am.auth_user(
                self.root_username,
                self.root_password + 'bar'
            )

    def test_auth_with_nonexistent_user(self):
        am = self._get_auth_manager_with_root()

        with self.assertRaises(ValueError):
            am.auth_user(
                self.root_username + '_bar',
                self.root_password
            )

    def test_normal_user_creation_by_root(self):
        am = self._get_auth_manager_with_root()

        root_token = am.auth_user(
            self.root_username,
            self.root_password
        )

        am.create_user(
            token=root_token,
            username=self.sample_user_name,
            password=self.sample_user_password
        )

    def test_normal_user_creation_duplicate(self):
        am = self._get_auth_manager_with_root()

        root_token = am.auth_user(
            self.root_username,
            self.root_password
        )

        with self.assertRaises(ValueError):
            am.create_user(
                token=root_token,
                username=self.root_username,
                password=self.root_password + 'bar'
            )

    def test_only_root_can_create_users(self):
        am, root_token = self._get_auth_manager_with_sample_user()

        sample_user_token = am.auth_user(
            username=self.sample_user_name,
            password=self.sample_user_password
        )

        with self.assertRaises(ValueError):
            am.create_user(
                token=sample_user_token,
                username=self.sample_user_name + '_bar',
                password=self.sample_user_password
            )

    def test_user_deletion(self):
        am, root_token = self._get_auth_manager_with_sample_user()

        am.remove_user(
            token=root_token,
            username=self.sample_user_name
        )

    def test_root_cant_be_deleted(self):
        am, root_token = self._get_auth_manager_with_sample_user()

        with self.assertRaises(ValueError):
            am.remove_user(
                root_token,
                self.root_username
            )

    def test_only_root_can_delete_users(self):
        am, root_token = self._get_auth_manager_with_sample_user()

        sample_user_token = am.auth_user(
            username=self.sample_user_name,
            password=self.sample_user_password
        )

        am.create_user(
            token=root_token,
            username=self.sample_user_2_name,
            password=self.sample_user_password
        )

        with self.assertRaises(ValueError):
            am.remove_user(
                sample_user_token,
                self.sample_user_2_name
            )

if __name__ == '__main__':
    unittest.main()
