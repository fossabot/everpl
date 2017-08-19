# Include standard modules
import asyncio
import logging

# Include 3rd-party modules
# Include DPL modules
from dpl import api
from dpl import auth
from dpl.core import Configuration
from dpl.core.platform_manager import PlatformManager


class Controller(object):
    def __init__(self):
        self._conf = Configuration(path="../samples/config")
        self._pm = PlatformManager()

        self._auth_manager = auth.AuthManager()

        self._api_gateway = api.ApiGateway(self._auth_manager)
        self._rest_api = api.RestApi(self._api_gateway)

    async def start(self):
        self._conf.load_config()

        core_settings = self._conf.get_by_subsystem("core")
        connection_settings = self._conf.get_by_subsystem("connections")
        thing_settings = self._conf.get_by_subsystem("things")

        enabled_platforms = core_settings["enabled_platforms"]

        self._pm.init_platforms(enabled_platforms)
        self._pm.init_connections(connection_settings)
        self._pm.init_things(thing_settings)

        self._pm.enable_all_things()

        # FIXME: Only for testing purposes
        self._auth_manager.create_root_user("admin", "admin")

        asyncio.ensure_future(
            self._rest_api.create_rest_server()
        )

    async def shutdown(self):
        # await self._api_application.shutdown()
        self._pm.disable_all_things()
