# Include standard modules
import asyncio
import logging

# Include 3rd-party modules
# Include DPL modules
from adpl import api


class Controller(object):
    def __init__(self):
        pass

    async def start(self):
        loop = asyncio.get_event_loop()

        asyncio.ensure_future(
            api.create_rest_server(loop=loop)
        )

    async def shutdown(self):
        # await self._api_application.shutdown()
        pass
