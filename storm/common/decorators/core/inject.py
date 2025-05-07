from typing import Any, Optional

from storm.common.constants import (
    PARAMTYPES_METADATA,
    PROPERTY_DEPS_METADATA,
    SELF_DECLARED_DEPS_METADATA,
)
from storm.core.di.reflect import Reflect


class Inject:
    """
    Decorator that marks a class property or constructor parameter for injection.

    Can be used as:
        @Inject()              -> attempts to infer the token
        @Inject(MyToken)       -> uses the explicit token

    Supports both property and parameter decorators.
    """

    def __init__(self, token: Optional[Any] = None):
        self.token = token

    def __call__(self, target: object, key: Optional[str] = None, index: Optional[int] = None):
        if index is not None:
            # Constructor parameter
            inferred_type = self.token
            if inferred_type is None:
                paramtypes = Reflect.get_metadata(PARAMTYPES_METADATA, target)
                if paramtypes and len(paramtypes) > index:
                    inferred_type = paramtypes[index]

            deps = Reflect.get_metadata(SELF_DECLARED_DEPS_METADATA, target) or []
            deps.append({"index": index, "param": inferred_type})
            Reflect.define_metadata(SELF_DECLARED_DEPS_METADATA, deps, target)
        else:
            # Property injection
            inferred_type = self.token
            if inferred_type is None:
                inferred_type = Reflect.get_metadata("design:type", target, key)

            cls = target if isinstance(target, type) else target.__class__
            props = Reflect.get_metadata(PROPERTY_DEPS_METADATA, cls) or []
            props.append({"key": key, "type": inferred_type})
            Reflect.define_metadata(PROPERTY_DEPS_METADATA, props, cls)
