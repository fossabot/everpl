"""
This module contains a definition of DeliveryManager - of a class which
controls delivery of the messages and stores all the undelivered messages
"""
import asyncio
import logging
from typing import Dict, Optional
from collections import OrderedDict

from dpl.model.domain_id import TDomainId
from .message import Message


LOGGER = logging.getLogger(__name__)


def clear_queue(queue: asyncio.Queue) -> None:
    """
    Removes all elements from the specified Queue

    :param queue: a Queue to be cleared
    :return: None
    """
    try:
        while not queue.empty():
            queue.get_nowait()
    except asyncio.QueueEmpty:
        LOGGER.error("Multitasking issue: something exhausted the queue while "
                     "queue cleaning was in progress")


class RescheduledItem(object):
    """
    RescheduledItem is structure data type used for storage of information for
    re-scheduled (i.e. not acknowledged) Tracked Messages. The information to
    be saved is a message itself, a re-scheduling task and a number of
    re-schedules already performed.
    """

    def __init__(
            self, message: Message,
            delayed_reschedule: Optional[asyncio.Future] = None,
            number_of_reschedules: int = 0
    ):
        """
        Constructor. Sets the specified field values

        :param message: a message to be sent
        :param delayed_reschedule: a Task for a coroutine that adds a message
               back to the queue of pending messages after some delay
        :param number_of_reschedules: number of re-schedule attempts
               already performed
        """
        assert message.message_id is not None
        self.message = message
        self.delayed_reschedule = delayed_reschedule
        self.number_of_reschedules = number_of_reschedules


class SessionRetainedStorage(object):
    """
    A structure that contains information about the list of retained
    undelivered messages, the number of retransmissions already performed and
    the Future that is currently handling retransmissions for this Session
    """
    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        """
        Constructor. Sets all fields to their default values. Creates an
        asyncio lock with the specified loop

        :param loop: an instance of EventLoop to be used for asyncio Lock
               instantiation
        """
        self.messages = OrderedDict()  # type: OrderedDict[int, Message]
        self.n_of_retransmissions = 0
        self.retransmission_handler = None  # type: Optional[asyncio.Future]
        self.messages_lock = asyncio.Lock(loop=None)
        self.last_message_number = 0


# SessionRescheduledRegistry is Mapping of a unique message identifier and
# items of information about re-schedules
SessionRescheduledRegistry = Dict[int, RescheduledItem]


class DeliveryManager(object):
    """
    This class controls the delivery of all messages outcoming from a server.
    It stores all undelivered messages, provides a queue of pending messages,
    control acknowledgements and automatically re-schedules delivery of
    unacknowledged messages if the delivery was not acknowledged by a client
    """
    MAX_MESSAGE_ID = 65536
    MAX_RETRANSMISSION_DELAY = 14400

    def __init__(self, *, loop: asyncio.AbstractEventLoop = None):
        """
        Constructor. Receives an instance of EventLoop that will handle message
        re-scheduling and will be bonded with a queue of pending messages.
        Initializes internal variables.

        :param loop: an instance of EventLoop that will be used for message
               re-scheduling and that will be associated with a message queue
        """
        self._loop = loop

        # contains a query of ready-to-be-sent messages for each opened session
        self._pending_messages = dict()  # type: Dict[TDomainId, asyncio.Queue]

        # contains a per-session registry of unacknowledged messages and
        # related information
        self._retained = dict()  # type: Dict[TDomainId,SessionRetainedStorage]

    async def get_message(self, session_id: TDomainId) -> Message:
        """
        Attempts to extract the new message from a queue of pending messages.
        Blocks if there is not pending messages in the queue

        :param session_id: an identifier of Session for which the new message
               must to be retrieved
        :return: a new message from a queue of pending message
        :raises KeyError: if a queue for the specified Session can't be found
        """
        session_queue = self._pending_messages.setdefault(
            session_id, asyncio.Queue(loop=self._loop)
        )

        result = await session_queue.get()
        session_queue.task_done()
        return result

    async def put_message(
            self, session_id: TDomainId, message: Message,
            ensure_delivery: bool = False
    ) -> None:
        """
        Attempts to put a new message in a queue of pending messages for the
        specified Session. Blocks if the maximum number of pending messages
        was reached

        :param session_id: an identifier of Session for which the new message
               must to be added to the list of pending messages
        :param message: a message to be added to the list of pending messages
               for this Session
        :param ensure_delivery: if the delivery of this message must to be
               acknowledged by client
        :return: None
        """
        await self._add_to_pending(session_id=session_id, message=message)

        if ensure_delivery:
            await self._add_to_retained(session_id=session_id, message=message)

    async def ack_delivery(
            self, session_id: TDomainId, message_id: int
    ) -> None:
        """
        Acknowledges the delivery of a TrackedMessage. Removes the message
        with the specified ID from the list of rescheduled messages

        :param session_id: an identifier of Session for which the message
               must to be acknowledged
        :param message_id: an identifier of a message to be acknowledged
        :return: None
        """
        session_retained = self._retained.get(session_id)

        if session_retained is None:
            LOGGER.warning(
                "Acknowledge received for a closed or unopened Session: %s. "
                "Message #%d", session_id, message_id)
            return

        async with session_retained.messages_lock:
            if message_id in session_retained.messages:
                session_retained.messages.pop(message_id)
                session_retained.n_of_retransmissions = 0
            else:
                LOGGER.info(
                    "Message #%d was already acknowledged, ignored. "
                    "Session %s.", message_id, session_id
                )

    async def pause_for(self, session_id: TDomainId) -> None:
        """
        Pauses delivery for the specified Session. Clears the queue of pending
        messages

        :param session_id: an identifier of Session for which communication
               must to be paused
        :return: None
        """
        session_retained = self._retained.get(session_id)

        if session_retained is not None:
            assert session_retained.retransmission_handler is not None
            session_retained.retransmission_handler.cancel()
            # await session_retained.retransmission_handler

        queue = self._pending_messages.get(session_id)

        if queue is not None:
            clear_queue(queue)

    async def resume_for(self, session_id: TDomainId) -> None:
        """
        Adds back all undelivered messages to the queue of pending messages

        :param session_id: an identifier of Session for which communication
               must to be resumed
        :return: None
        """
        session_retained = self._retained.setdefault(
            session_id, SessionRetainedStorage()
        )

        session_retained.n_of_retransmissions = 0
        old_handler = session_retained.retransmission_handler

        if old_handler is not None and not old_handler.done():
            LOGGER.warning(
                "The old session retransmission task was still alive for "
                "%s Session. Old connection is dead?", session_id
            )
            old_handler.cancel()

        session_retained.retransmission_handler = asyncio.ensure_future(
            self._retransmission_handler(session_id, session_retained),
            loop=self._loop
        )

    async def discard_for(self, session_id: TDomainId) -> None:
        """
        Stops all retransmissions and discard all stored data for the specified
        Session

        :param session_id: an identifier of Session we need to forget about
        :return: None
        """
        await self.pause_for(session_id)

        if session_id in self._pending_messages:
            self._pending_messages.pop(session_id)

        if session_id in self._retained:
            self._retained.pop(session_id)

    async def _add_to_pending(
            self, session_id: TDomainId, message: Message
    ) -> None:
        """
        Adds a Message to the list of pending (on delivery) messages

        :param session_id: an identifier of Session for which the new message
               must to be added to the list of pending messages
        :param message: a message to be added to the list of pending messages
               for this Session
        :return: None
        """
        session_queue = self._pending_messages.setdefault(
            session_id, asyncio.Queue(loop=self._loop)
        )
        await session_queue.put(message)
        LOGGER.debug(
            "Pending %d messages for %s", session_queue.qsize(), session_id
        )

    async def _add_to_retained(
            self, session_id: TDomainId, message: Message
    ) -> None:
        """
        Adds a Message to the list of retained messages

        :param session_id: an identifier of Session for which the new message
               must to be added to the list of retained messages
        :param message: a message to be added to the list of retained messages
               for this Session
        :return: None
        """
        assert message.message_id is None

        session_retained = self._retained.setdefault(
            session_id, SessionRetainedStorage()
        )

        if session_retained.retransmission_handler is None:
            session_retained.retransmission_handler = asyncio.ensure_future(
                self._retransmission_handler(session_id, session_retained),
                loop=self._loop
            )

        async with session_retained.messages_lock:
            last_message_id = session_retained.last_message_number
            message.message_id = (last_message_id + 1) % self.MAX_MESSAGE_ID
            session_retained.last_message_number = last_message_id
            session_retained.messages[message.message_id] = message

    async def _retransmission_handler(
            self, session_id: TDomainId,
            session_retained: SessionRetainedStorage
    ) -> None:
        """
        Watches the list of retained messages and adds them to the queue of
        to-be-sent (pending) messages after some delay. Delay is growing
        with a number of retransmission attempts already performed

        :param session_id: an identifier of Session this handler is assigned to
        :param session_retained: information about retained messages and
               retransmissions performed by this handler
        :return: None
        """
        delay = 1

        while True:  # interrupted with future cancellation
            delay = min(delay * 2, self.MAX_RETRANSMISSION_DELAY)
            await asyncio.sleep(delay, loop=self._loop)

            async with session_retained.messages_lock:
                for message in session_retained.messages.values():
                    await self._add_to_pending(session_id, message)

            session_retained.n_of_retransmissions += 1
