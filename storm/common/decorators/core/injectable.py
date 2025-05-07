# storm/decorators/injectable.py

import uuid
from typing import Optional, Type

from storm.common.constants import INJECTABLE_WATERMARK, SCOPE_OPTIONS_METADATA
from storm.common.interfaces.scope_options import Scope
from storm.core.di.reflect import Reflect


class Injectable:
    """
    Class decorator that marks a class as injectable in the Storm DI container.

    :param scope: Optional scope (DEFAULT, REQUEST, TRANSIENT)
    :param durable: Whether this injectable is durable (lazy subtree)
    """

    def __init__(self, scope: Optional[Scope] = None, durable: Optional[bool] = None):
        self.scope = scope
        self.durable = durable

    def __call__(self, cls: Type) -> Type:
        Reflect.define_metadata(INJECTABLE_WATERMARK, True, cls)
        if self.scope or self.durable:
            Reflect.define_metadata(
                SCOPE_OPTIONS_METADATA,
                {"scope": self.scope, "durable": self.durable},
                cls,
            )
        return cls


class Mixin:
    """
    Class decorator that assigns a unique name to the class and marks it as Injectable.
    """

    def __init__(self):
        self.name = f"Mixin_{uuid.uuid4().hex[:12]}"

    def __call__(self, cls: Type) -> Type:
        cls.__name__ = self.name
        return Injectable()(cls)
