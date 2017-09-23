# Include standard modules
import asyncio
import os

# Include 3rd-party modules
# Include DPL modules
from dpl import DPL_INSTALL_PATH
from dpl import api
from dpl import auth
from dpl.core import Configuration
from dpl.integrations import BindingManager
from dpl.core.placement_manager import PlacementManager


class Controller(object):
    def __init__(self):
        os.path.abspath(__file__)

        self._conf = Configuration(path=os.path.join(DPL_INSTALL_PATH, "../samples/config"))
        self._placements = PlacementManager()
        self._bm = BindingManager()

        self._auth_manager = auth.AuthManager()

        self._api_gateway = api.ApiGateway(self._auth_manager, self._bm, self._placements)
        self._rest_api = api.RestApi(self._api_gateway)

    async def start(self):
        self._conf.load_config()

        core_settings = self._conf.get_by_subsystem("core")
        placement_settings = self._conf.get_by_subsystem("placements")
        connection_settings = self._conf.get_by_subsystem("connections")
        thing_settings = self._conf.get_by_subsystem("things")

        self._placements.init_placements(placement_settings)

        enabled_integrations = core_settings["enabled_integrations"]

        self._bm.init_integrations(enabled_integrations)
        self._bm.init_connections(connection_settings)
        self._bm.init_things(thing_settings)

        self._bm.enable_all_things()

        # FIXME: Only for testing purposes
        self._auth_manager.create_root_user("admin", "admin")

        asyncio.ensure_future(
            self._rest_api.create_server(host="0.0.0.0", port=10800)
        )

    async def shutdown(self):
        await self._rest_api.shutdown_server()
        self._bm.disable_all_things()
