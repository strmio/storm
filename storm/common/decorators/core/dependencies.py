from typing import Any, Callable, Sequence, Type

from storm.common.constants import PARAMTYPES_METADATA
from storm.core.di.reflect import Reflect


def flatten(arr: Sequence[Any]) -> list[Any]:
    """
    Recursively flattens a nested sequence.

    :param arr: A (possibly nested) list or tuple.
    :return: A flat list.
    """
    flat = []
    for item in arr:
        if isinstance(item, (list, tuple)):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat


def Dependencies(*dependencies: Any) -> Callable[[Type], Type]:
    """
    Decorator that assigns a flattened list of dependencies
    to the class using PARAMTYPES_METADATA.

    :param dependencies: Dependencies required by the class.
    :return: Class decorator.
    """
    flat_deps = flatten(dependencies)

    def decorator(cls: Type) -> Type:
        Reflect.define_metadata(PARAMTYPES_METADATA, flat_deps, cls)
        return cls

    return decorator
