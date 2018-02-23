import unittest
from unittest.mock import Mock

from dpl.auth.auth_context import AuthContext
from dpl.auth.abs_auth_service import AbsAuthService
from dpl.repo_impls.in_memory.placement_repository import PlacementRepository
from dpl.service_impls.placement_service import PlacementService
from dpl.auth.auth_aspect import AuthAspect, AuthMissingTokenError
from dpl.utils.simple_interceptor import SimpleInterceptor
from dpl.utils.generate_token import generate_token


class TestAuthAspect(unittest.TestCase):
    def setUp(self):
        self.auth_service = Mock(spec=AbsAuthService)  # type: AbsAuthService
        self.auth_service.check_permission = Mock()

        self.auth_context = AuthContext()
        self.auth_aspect = AuthAspect(
            auth_service=self.auth_service,
            auth_context=self.auth_context
        )
        self.placement_repo = PlacementRepository()
        self.placement_service = PlacementService(self.placement_repo)
        self.protected_service = SimpleInterceptor(
            wrapped=self.placement_service,
            aspect=self.auth_aspect
        )  # type: PlacementService

        self.sample_token = generate_token()

    def test_permission_checked(self):
        """
        Tests that a random method of a protected service (or
        some another class) was correctly intercepted, access
        token with other contextual information was extracted
        and passed to the AuthService's check_permission method

        :return: None
        """
        with self.auth_context(token=self.sample_token):
            self.protected_service.view_all()

        mocked_method = self.auth_service.check_permission  # type: Mock
        mocked_method.assert_called_with(
            access_token=self.sample_token,
            in_domain='PlacementService',
            to_execute='view_all',
            args=(),
            kwargs=dict()
        )

    def test_call_arguments_passed(self):
        """
        Tests that on permission checking all call arguments
        was intercepted and passed to the authorization
        checker

        :return: None
        """
        placement_name = "Some Placement"
        placement_image = None

        with self.auth_context(token=self.sample_token):
            self.protected_service.create_placement(
                placement_name,
                image_url=placement_image
            )

        mocked_method = self.auth_service.check_permission  # type: Mock
        mocked_method.assert_called_with(
            access_token=self.sample_token,
            in_domain='PlacementService',
            to_execute='create_placement',
            args=(placement_name,),
            kwargs={'image_url': placement_image}
        )

    def test_out_of_context_error(self):
        """
        Tests that if an access token is missing in an
        AuthContext, then an FIXME error will be raised

        :return: None
        """
        with self.assertRaises(AuthMissingTokenError):
            self.protected_service.view_all()
