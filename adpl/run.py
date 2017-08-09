# Include standard modules
import asyncio
import logging

# Include 3rd-party modules
# Include DPL modules
from adpl.core import Controller


# Init processes

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def shutdown(loop: asyncio.AbstractEventLoop = None):
    """
    Shutdown: Cancel all pending tasks and wait for them to complete
    :param loop: EventLoop where tasks are running in
    :return: None
    """
    all_tasks = asyncio.Task.all_tasks(loop)  # type: set[asyncio.Task]

    for task in all_tasks:
        task.cancel()

    try:
        loop.run_until_complete(
            asyncio.gather(*all_tasks)
        )
    except asyncio.CancelledError:
        pass


def main():
    """
    Main function of the application
    :return: None
    """
    loop = asyncio.get_event_loop()

    try:
        loop.set_debug(enabled=True)
        controller = Controller()

        asyncio.ensure_future(controller.setup(), loop=loop)
        loop.run_forever()

    except KeyboardInterrupt:
        pass

    finally:
        shutdown(loop)
        loop.close()


if __name__ == "__main__":
    main()
