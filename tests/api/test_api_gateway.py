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

    def test_auth_success(self):
        auth_manager_mock = mock.Mock(spec_set=AuthManager)
        binding_manager_mock = mock.Mock(spec_set=BindingManager)
        placement_manager_mock = mock.Mock(spec_set=PlacementManager)

        test_token = generate_token()

        auth_manager_mock.auth_user = mock.Mock()
        auth_manager_mock.auth_user.return_value = test_token

        gateway = ApiGateway(
            auth_manager_mock,
            binding_manager_mock,
            placement_manager_mock
        )

        test_username = "test"
        test_password = "pass"

        token = gateway.auth(username=test_username, password=test_password)

        auth_manager_mock.auth_user.assert_called_once_with(
            test_username, test_password
        )

        self.assertEqual(token, test_token)

    def test_getters_invalid_token(self):
        auth_manager_mock = mock.Mock(spec_set=AuthManager)
        binding_manager_mock = mock.Mock(spec_set=BindingManager)
        placement_manager_mock = mock.Mock(spec_set=PlacementManager)

        auth_manager_mock.is_token_valid = mock.Mock()
        auth_manager_mock.is_token_valid.return_value = False

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"
        test_unregistered_cmd = "nobody cares"

        gateway = ApiGateway(
            auth_manager_mock,
            binding_manager_mock,
            placement_manager_mock
        )

        with self.assertRaises(exceptions.InvalidTokenError):
            gateway.get_things(test_unregistered_token)

        with self.assertRaises(exceptions.InvalidTokenError):
            gateway.get_thing(test_unregistered_token, test_unregistered_id)

        with self.assertRaises(exceptions.InvalidTokenError):
            gateway.get_placements(test_unregistered_token)

        with self.assertRaises(exceptions.InvalidTokenError):
            gateway.get_placement(test_unregistered_token, test_unregistered_id)

        with self.assertRaises(exceptions.InvalidTokenError):
            gateway.send_command(test_unregistered_token, test_unregistered_id, test_unregistered_cmd)

    def test_getters_insufficient_permissions_token(self):
        auth_manager_mock = mock.Mock(spec_set=AuthManager)
        binding_manager_mock = mock.Mock(spec_set=BindingManager)
        placement_manager_mock = mock.Mock(spec_set=PlacementManager)

        auth_manager_mock.is_token_valid = mock.Mock()
        auth_manager_mock.is_token_valid.return_value = True

        auth_manager_mock.is_token_grants = mock.Mock()
        auth_manager_mock.is_token_grants.return_value = False

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"
        test_unregistered_cmd = "nobody cares"

        gateway = ApiGateway(
            auth_manager_mock,
            binding_manager_mock,
            placement_manager_mock
        )

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            gateway.get_things(test_unregistered_token)

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            gateway.get_thing(test_unregistered_token, test_unregistered_id)

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            gateway.get_placements(test_unregistered_token)

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            gateway.get_placement(test_unregistered_token, test_unregistered_id)

        with self.assertRaises(exceptions.PermissionDeniedForTokenError):
            gateway.send_command(test_unregistered_token, test_unregistered_id, test_unregistered_cmd)

    def test_get_thing(self):
        auth_manager_mock = mock.Mock(spec_set=AuthManager)
        binding_manager_mock = mock.Mock(spec_set=BindingManager)
        placement_manager_mock = mock.Mock(spec_set=PlacementManager)

        auth_manager_mock.is_token_valid = mock.Mock()
        auth_manager_mock.is_token_valid.return_value = True

        auth_manager_mock.is_token_grants = mock.Mock()
        auth_manager_mock.is_token_grants.return_value = True

        test_thing = self.get_test_thing()

        binding_manager_mock.fetch_thing = mock.Mock()
        binding_manager_mock.fetch_thing.return_value = test_thing

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"

        gateway = ApiGateway(
            auth_manager_mock,
            binding_manager_mock,
            placement_manager_mock
        )

        result = gateway.get_thing(
            test_unregistered_token, test_unregistered_id
        )

        test_thing_dict = obj_to_dict(test_thing)
        test_thing_dict.update(test_thing.metadata)
        test_thing_dict.pop("metadata")

        # FIXME: Remove deprecated property
        test_thing_dict["description"] = test_thing_dict["friendly_name"]

        self.assertEqual(result, test_thing_dict)

    def test_get_placement(self):
        auth_manager_mock = mock.Mock(spec_set=AuthManager)
        binding_manager_mock = mock.Mock(spec_set=BindingManager)
        placement_manager_mock = mock.Mock(spec_set=PlacementManager)

        auth_manager_mock.is_token_valid = mock.Mock()
        auth_manager_mock.is_token_valid.return_value = True

        auth_manager_mock.is_token_grants = mock.Mock()
        auth_manager_mock.is_token_grants.return_value = True

        test_placement = self.get_test_placement()

        placement_manager_mock.fetch_placement = mock.Mock()
        placement_manager_mock.fetch_placement.return_value = test_placement

        test_unregistered_token = "nobody cares"
        test_unregistered_id = "nobody cares"

        gateway = ApiGateway(
            auth_manager_mock,
            binding_manager_mock,
            placement_manager_mock
        )

        result = gateway.get_placement(
            test_unregistered_token, test_unregistered_id
        )

        test_placement_dict = obj_to_dict(test_placement)

        test_placement_dict["id"] = test_placement_dict.pop("placement_id")

        # FIXME: Remove deprecated properties
        test_placement_dict["description"] = test_placement_dict["friendly_name"]
        test_placement_dict["image"] = test_placement_dict["image_url"]

        self.assertEqual(result, test_placement_dict)


if __name__ == '__main__':
    unittest.main()
