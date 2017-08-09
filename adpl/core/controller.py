# Include standard modules
import asyncio
import logging

# Include 3rd-party modules
# Include DPL modules


class Controller(object):
    def __init__(self):
        pass

    async def _hello_world(self):
        print("Hello, world!")
        await asyncio.sleep(10)

    async def setup(self):
        await self._hello_world()
