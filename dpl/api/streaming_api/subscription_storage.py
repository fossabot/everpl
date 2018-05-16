"""
This module contains a definition of SubscriptionStorage
"""

from typing import Dict, Set, List, Tuple, Optional, KeysView

from dpl.model.domain_id import TDomainId
from dpl.events.topic import topic_to_list


class SubscriptionStorage(object):
    """
    This object is responsible for storage of subscriptions and their
    management. Allows to add, remove and check subscriptions for the
    specified sessions
    """
    def __init__(self):
        """
        Constructor. Initializes internal storage
        """
        self._subs_tree = {}  # type: Dict[TDomainId, Dict]
        self._plain_subs = {}  # type: Dict[TDomainId, Set[str]]

    def list_sessions(self) -> KeysView[TDomainId]:
        """
        Returns the list of all Sessions currently registered as subscribers

        :return: identifiers of all Sessions that have subscribed to any topic
        """
        return self._plain_subs.keys()

    def add_subscription(
            self, session_id: TDomainId, topic: str, is_retained: bool = False
    ) -> None:
        """
        Adds a new subscription for the specified Session

        :param session_id: a unique identifier of Session
        :param topic: a topic this Session is subscribed to
        :param is_retained: are messages must to be retained for this topic
        :return: None
        """
        subs_for_session = self._plain_subs.setdefault(session_id, set())

        if topic in subs_for_session:
            return

        subs_for_session.add(topic)
        topic_parts = topic_to_list(topic)

        p_current = self._subs_tree.setdefault(session_id, dict())

        for part in topic_parts:
            p_current = p_current.setdefault(part, {})

        p_current[None] = is_retained

    @staticmethod
    def _remove_empty_nodes(chain: List[Tuple[Dict, str]]) -> None:
        """
        Removes all nodes without children from the chain of nodes, starting
        from the last node in the chain

        :param chain: a list of nodes to be cleaned
        :return: None
        """
        for container, value in reversed(chain):
            sub_container = container[value]

            if not sub_container:  # if sub-container is empty...
                container.pop(value)  # ...remove container

    def remove_subscription(self, session_id: TDomainId, topic: str) -> None:
        """
        Removes a subscription for the specified Session

        :param session_id: a unique identifier of Session
        :param topic: a topic for which unsubscription was requested
        :return: None
        """
        subs_for_session = self._plain_subs.setdefault(session_id, set())

        if topic not in subs_for_session:
            return

        topic_parts = topic_to_list(topic)

        # this list contains a chain of subscription tree nodes,
        # will be used for backward traversal and node removal
        chain = list()  # type: List[Tuple[Dict, str]]

        p_current = self._subs_tree.setdefault(session_id, dict())

        for part in topic_parts:
            chain.append((p_current, part))
            p_current = p_current[part]

        del p_current[None]

        self._remove_empty_nodes(chain=chain)

        subs_for_session.remove(topic)

    def remove_all_for(self, session_id: TDomainId) -> None:
        """
        Removes all subscriptions for the specified Session

        :param session_id: an identifier of Session which subscriptions will
               be removed
        :return: None
        """
        self._plain_subs.pop(session_id)
        self._subs_tree.pop(session_id)

    def resolve_subscription_params(
            self, session_id: TDomainId, topic: str
    ) -> Optional[bool]:
        """
        Attempts to find parameters of subscription corresponding to the
        specified Message topic

        :param session_id: an identifier of the session for which subscription
               will be checked
        :param topic: a topic of the message
        :return: None if the corresponding subscription wasn't found; True if
                 message retention was activated for this topic,
                 False otherwise
        """
        topic_parts = topic_to_list(topic)
        session_subs = self._subs_tree.get(session_id)

        p_current = session_subs

        for part in topic_parts:
            if part in p_current:
                p_current = p_current[part]
            elif '+' in p_current:
                p_current = p_current['+']
            elif '#' in p_current:
                p_current = p_current['#']
                break
            else:
                return None

        return p_current[None]

    def is_subscribed(self, session_id: TDomainId, topic: str) -> bool:
        """
        Checks if the specified Session has a Subscription, corresponding to
        the specified topic

        :param session_id: an identifier of the session for which subscription
               will be checked
        :param topic: a topic of the message
        :return: True if there is a subscription, False otherwise
        """
        resolved = self.resolve_subscription_params(
            session_id=session_id, topic=topic
        )

        return resolved is not None
