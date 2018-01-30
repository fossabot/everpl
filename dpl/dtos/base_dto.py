"""
This module contains definition of the base DTO (data
transfer object) class used to exchange information
between Services and their clients.

For now a simple Python dictionary type (actually, an
immutable Mapping type) with keys as strings (field
names) and anything as values is used as a DTO type.
"""
from typing import Mapping, Any


BaseDto = Mapping[str, Any]
