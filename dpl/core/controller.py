# Include standard modules
import asyncio

# Include 3rd-party modules
# Include DPL modules
from dpl import api
from dpl import auth
from dpl.core import Configuration
from dpl.platforms import PlatformManager
from dpl.core.placement_manager import PlacementManager


class Controller(object):
    def __init__(self):
        self._conf = Configuration(path="../samples/config")
        self._placements = PlacementManager()
        self._pm = PlatformManager()

        self._auth_manager = auth.AuthManager()

        self._api_gateway = api.ApiGateway(self._auth_manager, self._pm, self._placements)
        self._rest_api = api.RestApi(self._api_gateway)

    async def start(self):
        self._conf.load_config()

        core_settings = self._conf.get_by_subsystem("core")
        placement_settings = self._conf.get_by_subsystem("placements")
        connection_settings = self._conf.get_by_subsystem("connections")
        thing_settings = self._conf.get_by_subsystem("things")

        self._placements.init_placements(placement_settings)

        enabled_platforms = core_settings["enabled_platforms"]

        self._pm.init_platforms(enabled_platforms)
        self._pm.init_connections(connection_settings)
        self._pm.init_things(thing_settings)

        self._pm.enable_all_things()

        # FIXME: Only for testing purposes
        self._auth_manager.create_root_user("admin", "admin")

        asyncio.ensure_future(
            self._rest_api.create_server(host='localhost', port=10800)
        )

    async def shutdown(self):
        await self._rest_api.shutdown_server()
        self._pm.disable_all_things()
