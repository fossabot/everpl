# Include standard modules
import asyncio
import os

# Include 3rd-party modules
# Include DPL modules
from dpl import DPL_INSTALL_PATH
from dpl import api
from dpl import auth
from dpl.core import Configuration
from dpl.integrations.binding_bootstrapper import BindingBootstrapper
from dpl.placements.placement_bootstrapper import PlacementBootstrapper

from dpl.repo_impls.in_memory.placement_repository import PlacementRepository
from dpl.repo_impls.in_memory.connection_repository import ConnectionRepository
from dpl.repo_impls.in_memory.thing_repository import ThingRepository

from dpl.service_impls.placement_service import PlacementService
from dpl.service_impls.thing_service import ThingService


class Controller(object):
    def __init__(self):
        os.path.abspath(__file__)

        self._conf = Configuration(path=os.path.join(DPL_INSTALL_PATH, "../samples/config"))

        self._placement_repo = PlacementRepository()
        self._connection_repo = ConnectionRepository()
        self._thing_repo = ThingRepository()

        self._placement_service = PlacementService(self._placement_repo)
        self._thing_service = ThingService(self._thing_repo)

        self._auth_manager = auth.AuthManager()

        self._api_gateway = api.ApiGateway(self._auth_manager, self._thing_service, self._placement_service)
        self._rest_api = api.RestApi(self._api_gateway)

    async def start(self):
        self._conf.load_config()

        core_settings = self._conf.get_by_subsystem("core")
        placement_settings = self._conf.get_by_subsystem("placements")
        connection_settings = self._conf.get_by_subsystem("connections")
        thing_settings = self._conf.get_by_subsystem("things")

        PlacementBootstrapper.init_placements(
            placement_repo=self._placement_repo,
            config=placement_settings
        )

        enabled_integrations = core_settings["enabled_integrations"]

        binding_bootstrapper = BindingBootstrapper(
            connection_repo=self._connection_repo,
            thing_repo=self._thing_repo
        )

        binding_bootstrapper.init_integrations(enabled_integrations)
        binding_bootstrapper.init_connections(connection_settings)
        binding_bootstrapper.init_things(thing_settings)

        self._thing_service.enable_all()

        # FIXME: Only for testing purposes
        self._auth_manager.create_root_user("admin", "admin")

        asyncio.ensure_future(
            self._rest_api.create_server(host="0.0.0.0", port=10800)
        )

    async def shutdown(self):
        await self._rest_api.shutdown_server()
        self._thing_service.disable_all()
