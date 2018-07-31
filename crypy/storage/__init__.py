"""
Provides a class as a common interface for all implemented storages API, using delegation.
"""

from enum import Enum


class Storage_Impl(Enum):
    Arctic = 1


class Storage:

    def __init__(self, implementation: Storage_Impl) -> Storage:
        if implementation == Storage_Impl.Arctic:
            from . import arctic
            self.impl = arctic.init_api()

