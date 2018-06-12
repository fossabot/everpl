from enum import Enum
from typing import Any

from dpl.model.domain_id import TDomainId


class ConditionalOperator(Enum):
    EQ = 0
    GT = 1
    GE = 2


class Condition(object):
    def __init__(
            self, thing_id: TDomainId, field_name: str,
            operator: ConditionalOperator, field_value: Any
    ):
        self._thing_id = thing_id
        self.field_name = field_name
        self.operator = operator
        self.field_value = field_value

    @property
    def thing_id(self) -> TDomainId:
        return self._thing_id
