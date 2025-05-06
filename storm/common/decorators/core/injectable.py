# storm/decorators/injectable.py

import uuid

from storm.common.constants import INJECTABLE_WATERMARK, SCOPE_OPTIONS_METADATA
from storm.common.interfaces.scope_options import Scope
from storm.core.di.reflect import Reflect


def Injectable(scope: Scope | None = None, durable: bool | None = None):
    """
    Decorator that marks a class as injectable.

    :param scope: Optional scope of the injectable (DEFAULT, TRANSIENT, REQUEST).
    :param durable: Whether the provider is durable (lazy subtree construction).
    :return: ClassDecorator
    """

    def decorator(cls):
        Reflect.define_metadata(INJECTABLE_WATERMARK, True, cls)
        if scope or durable:
            Reflect.define_metadata(SCOPE_OPTIONS_METADATA, {"scope": scope, "durable": durable}, cls)
        return cls

    return decorator


def Mixin(cls):
    """
    Wraps a class as a mixin with a unique name and makes it injectable.

    :param cls: The class to wrap
    :return: The same class, marked as injectable with a random name
    """
    cls.__name__ = f"Mixin_{uuid.uuid4().hex[:12]}"
    Injectable()(cls)
    return cls
