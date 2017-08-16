# Include standard modules
import asyncio
import logging

# Include 3rd-party modules
# Include DPL modules
from dpl import api
from dpl import auth


class Controller(object):
    def __init__(self):
        am = auth.AuthManager()

        # FIXME: Only for testing purposes
        am.create_root_user("admin", "admin")

        self._auth_manager = am

        self._api_gateway = api.ApiGateway(self._auth_manager)
        self._rest_api = api.RestApi(self._api_gateway)

    async def start(self):
        asyncio.ensure_future(
            self._rest_api.create_rest_server()
        )

    async def shutdown(self):
        # await self._api_application.shutdown()
        pass
