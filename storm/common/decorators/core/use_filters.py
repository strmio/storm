# storm/common/decorators/core/use_filters.py
from typing import Callable, Optional, Type, Union

from storm.common.constants import EXCEPTION_FILTERS_METADATA
from storm.common.utils.extend_metadata import extend_array_metadata
from storm.common.utils.shared import is_function
from storm.common.utils.validate_each import validate_each


def is_filter_valid(filter: object) -> bool:
    if not filter:
        return False

    if is_function(filter):
        try:
            instance = filter()
        except Exception:
            return False
        return hasattr(instance, "catch") and callable(getattr(instance, "catch", None))

    return hasattr(filter, "catch") and callable(getattr(filter, "catch", None))


def UseFilters(*filters: Union[Type, Callable]) -> Union[Callable, Type]:
    """
    Decorator that binds exception filters to the controller or method.

    :param filters: One or more filter classes or instances.
    :return: Decorator for class or method.
    """

    def decorator(
        target: Union[Callable, Type],
        key: Optional[str] = None,
        descriptor: Optional[Callable] = None,
    ) -> Union[Callable, Type]:
        if descriptor:
            validate_each(target.__class__, filters, is_filter_valid, "@UseFilters", "filter")
            extend_array_metadata(EXCEPTION_FILTERS_METADATA, list(filters), descriptor)
            return descriptor

        validate_each(target, filters, is_filter_valid, "@UseFilters", "filter")
        extend_array_metadata(EXCEPTION_FILTERS_METADATA, list(filters), target)
        return target

    return decorator
