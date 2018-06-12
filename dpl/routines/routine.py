from typing import Iterable, Optional

from dpl.model.base_entity import BaseEntity, TDomainId

from .action import Action
from .condition import Condition


class Routine(BaseEntity):
    def __init__(
            self,
            domain_id: TDomainId,
            sensitivity_list: Iterable[str],
            condition: Optional[Condition],
            actions: Iterable[Action],
            author_id: TDomainId,
            friendly_name: Optional[str] = None
    ):
        """

        :param domain_id:
        :param sensitivity_list:
        :param condition: set to None to disable condition checking
        :param actions:
        :param author_id:
        :param friendly_name:
        """

        super().__init__(domain_id)
        self.is_enabled = False
        self.sensitivity_list = tuple(sensitivity_list)
        self.friendly_name = friendly_name
        self._author_id = author_id
        self.actions = list(actions)
        self.condition = condition

    @property
    def author_id(self) -> TDomainId:
        return self._author_id
