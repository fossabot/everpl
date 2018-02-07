"""
This module just contains a definition of an empty
non-mutable mapping
"""

from types import MappingProxyType

EMPTY_MAPPING = MappingProxyType(dict())
