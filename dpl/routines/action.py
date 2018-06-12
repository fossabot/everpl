from typing import Mapping

from dpl.utils.empty_mapping import EMPTY_MAPPING
from dpl.model.domain_id import TDomainId


class Action(object):
    def __init__(
            self, thing_id: TDomainId,
            command: str, command_args: Mapping = EMPTY_MAPPING
    ):
        self.thing_id = thing_id
        self.command = command
        self.command_args = command_args
