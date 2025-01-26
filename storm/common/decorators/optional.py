from functools import wraps
from typing import Any

class OptionalMeta:
    def __init__(self, default: Any = None):
        self.default = default

def Optional(default: Any = None):
    """
    Marks a parameter as optional with an optional default value.
    """
    return OptionalMeta(default=default)
