from enum import Enum
from typing import Optional


class Scope(str, Enum):
    DEFAULT = "default"
    TRANSIENT = "transient"
    REQUEST = "request"


class ScopeOptions:
    def __init__(self, scope: Optional[Scope] = None, durable: Optional[bool] = None):
        self.scope = scope
        self.durable = durable
