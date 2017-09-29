# Include standard modules
import unittest
from unittest import mock
from inspect import signature

# Include 3rd-party modules

# Include DPL modules
from dpl.api import ApiGateway
from dpl.api import exceptions
from dpl.auth import AuthManager
from dpl.integrations import BindingManager
from dpl.placements import Placement, PlacementManager
from dpl.utils import generate_token, obj_to_dict
from dpl.things import Thing, Actuator
from dpl.connections import Connection

from dpl.integrations.dummy import DummySwitch, DummyConnection

# FIXME: CC16: Reduce code duplication
# FIXME: CC17: Add tests for several placements and several things in a list
# FIXME: CC18: Add tests for command sending (after stabilization of its API)
# FIXME: CC19: Replace DummySwitch with a Mock
# FIXME: CC20: Replace all Mocks with the real classes


class TestApiGateway(unittest.TestCase):
    GETTER_METHODS_LIST = [
        'get_things', 'get_thing',
        'get_placements', 'get_placement'
    ]

    @staticmethod
    def get_test_thing():
        connection_mock = mock.Mock(spec_set=DummyConnection)
        metadata = {
            "id": "Li1",
            "type": "switch",
            "friendly_name": "Corridor Lighting",
            "placement": "R1",
        }

        return DummySwitch(con_instance=connection_mock, con_params={"prefix": "test"}, metadata=metadata)

    @staticmethod
    def get_test_placement():
        return Placement(
            placement_id="R1",
            friendly_name="Corridor",
            image_url=None
        )

    def setUp(self):
        self.auth_manager_mock = mock.Mock(spec_set=AuthManager)
        self.binding_manager_mock = mock.Mock(spec_set=BindingManager)
        self.placement_manager_mock = mock.Mock(spec_set=PlacementManager)

        self.gateway = ApiGateway(
            self.auth_manager_mock,
            self.binding_manager_mock,
            self.placement_manager_mock
        )

    def tearDown(self):
        del self.gateway

        del self.auth_manager_mock
        del self.binding_manager_mock
        del self.placement_manager_mock

    def test_auth_success(self):
        test_token = generate_token()

        self.auth_manager_mock.auth_user = mock.Mock()
        self.auth_manager_mock.auth_user.return_value = test_token

        test_username = "test"
        test_password = "pass"

        token = self.gateway.auth(username=test_username, password=test_password)

        self.auth_manager_mock.auth_user.assert_called_once_with(
            test_username, test_password
        )

        self.assertEqual(token, test_token)

    def test_protected_invalid_token(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = False

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"
        test_unregistered_cmd = "nobody cares"

        with self.assertRaises(exceptions.InvalidTokenError):
            self.gateway.get_things(test_unregistered_token)

        with self.assertRaises(exceptions.InvalidTokenError):
            self.gateway.get_thing(test_unregistered_token, test_unregistered_id)

        with self.assertRaises(exceptions.InvalidTokenError):
            self.gateway.get_placements(test_unregistered_token)

        with self.assertRaises(exceptions.InvalidTokenError):
            self.gateway.get_placement(test_unregistered_token, test_unregistered_id)

        with self.assertRaises(exceptions.InvalidTokenError):
            self.gateway.send_command(test_unregistered_token, test_unregistered_id, test_unregistered_cmd)

    def test_protected_insufficient_permissions_token(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = True

        self.auth_manager_mock.is_token_grants = mock.Mock()
        self.auth_manager_mock.is_token_grants.return_value = False

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"
        test_unregistered_cmd = "nobody cares"

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            self.gateway.get_things(test_unregistered_token)

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            self.gateway.get_thing(test_unregistered_token, test_unregistered_id)

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            self.gateway.get_placements(test_unregistered_token)

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            self.gateway.get_placement(test_unregistered_token, test_unregistered_id)

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            self.gateway.send_command(test_unregistered_token, test_unregistered_id, test_unregistered_cmd)

    def test_get_thing(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = True

        self.auth_manager_mock.is_token_grants = mock.Mock()
        self.auth_manager_mock.is_token_grants.return_value = True

        test_thing = self.get_test_thing()

        self.binding_manager_mock.fetch_thing = mock.Mock()
        self.binding_manager_mock.fetch_thing.return_value = test_thing

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"

        result = self.gateway.get_thing(
            test_unregistered_token, test_unregistered_id
        )

        test_thing_dict = obj_to_dict(test_thing)
        test_thing_dict.update(test_thing.metadata)
        test_thing_dict.pop("metadata")

        # FIXME: Remove deprecated property
        test_thing_dict["description"] = test_thing_dict["friendly_name"]

        self.assertEqual(result, test_thing_dict)

    def test_get_nonexistent_thing(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = True

        self.auth_manager_mock.is_token_grants = mock.Mock()
        self.auth_manager_mock.is_token_grants.return_value = True

        def bm_fetch_side_effect(*args, **kwargs):
            raise KeyError

        self.binding_manager_mock.fetch_thing = mock.Mock()
        self.binding_manager_mock.fetch_thing.side_effect = bm_fetch_side_effect

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"

        with self.assertRaises(exceptions.ThingNotFoundError):
            self.gateway.get_thing(
                test_unregistered_token, test_unregistered_id
            )

    def test_get_empty_thing_list(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = True

        self.auth_manager_mock.is_token_grants = mock.Mock()
        self.auth_manager_mock.is_token_grants.return_value = True

        self.binding_manager_mock.fetch_all_things = mock.Mock()
        self.binding_manager_mock.fetch_all_things.return_value = []

        test_unregistered_token = "nobody cares"

        result = self.gateway.get_things(test_unregistered_token)

        self.assertEqual(result, [])

    def test_get_thing_list(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = True

        self.auth_manager_mock.is_token_grants = mock.Mock()
        self.auth_manager_mock.is_token_grants.return_value = True

        test_thing = self.get_test_thing()

        self.binding_manager_mock.fetch_all_things = mock.Mock()
        self.binding_manager_mock.fetch_all_things.return_value = [test_thing, ]

        test_unregistered_token = "nobody cares"

        test_thing_dict = obj_to_dict(test_thing)
        test_thing_dict.update(test_thing.metadata)
        test_thing_dict.pop("metadata")

        # FIXME: Remove deprecated property
        test_thing_dict["description"] = test_thing_dict["friendly_name"]

        result = self.gateway.get_things(test_unregistered_token)

        self.assertEqual(result, [test_thing_dict, ])

    def test_get_placement(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = True

        self.auth_manager_mock.is_token_grants = mock.Mock()
        self.auth_manager_mock.is_token_grants.return_value = True

        test_placement = self.get_test_placement()

        self.placement_manager_mock.fetch_placement = mock.Mock()
        self.placement_manager_mock.fetch_placement.return_value = test_placement

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"

        result = self.gateway.get_placement(
            test_unregistered_token, test_unregistered_id
        )

        test_placement_dict = obj_to_dict(test_placement)

        test_placement_dict["id"] = test_placement_dict.pop("placement_id")

        # FIXME: Remove deprecated properties
        test_placement_dict["description"] = test_placement_dict["friendly_name"]
        test_placement_dict["image"] = test_placement_dict["image_url"]

        self.assertEqual(result, test_placement_dict)

    def test_get_nonexistent_placement(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = True

        self.auth_manager_mock.is_token_grants = mock.Mock()
        self.auth_manager_mock.is_token_grants.return_value = True

        def pm_fetch_side_effect(*args, **kwargs):
            raise KeyError

        self.placement_manager_mock.fetch_placement = mock.Mock()
        self.placement_manager_mock.fetch_placement.side_effect = pm_fetch_side_effect

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"

        with self.assertRaises(exceptions.PlacementNotFoundError):
            self.gateway.get_placement(
                test_unregistered_token, test_unregistered_id
            )

    def test_get_empty_placement_list(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = True

        self.auth_manager_mock.is_token_grants = mock.Mock()
        self.auth_manager_mock.is_token_grants.return_value = True

        self.placement_manager_mock.fetch_all_placements = mock.Mock()
        self.placement_manager_mock.fetch_all_placements.return_value = []

        test_unregistered_token = "nobody cares"

        result = self.gateway.get_placements(test_unregistered_token)

        self.assertEqual(result, [])

    def test_get_placement_list(self):
        self.auth_manager_mock.is_token_valid = mock.Mock()
        self.auth_manager_mock.is_token_valid.return_value = True

        self.auth_manager_mock.is_token_grants = mock.Mock()
        self.auth_manager_mock.is_token_grants.return_value = True

        test_placement = self.get_test_placement()

        self.placement_manager_mock.fetch_all_placements = mock.Mock()
        self.placement_manager_mock.fetch_all_placements.return_value = [test_placement, ]

        test_unregistered_token = "nobody cares"

        test_placement_dict = obj_to_dict(test_placement)

        test_placement_dict["id"] = test_placement_dict.pop("placement_id")

        # FIXME: Remove deprecated properties
        test_placement_dict["description"] = test_placement_dict["friendly_name"]
        test_placement_dict["image"] = test_placement_dict["image_url"]

        result = self.gateway.get_placements(test_unregistered_token)

        self.assertEqual(result, [test_placement_dict, ])


if __name__ == '__main__':
    unittest.main()
