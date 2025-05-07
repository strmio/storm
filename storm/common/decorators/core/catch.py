# storm/decorators/catch.py

from typing import Any, Type

from storm.common.constants import CATCH_WATERMARK, FILTER_CATCH_EXCEPTIONS
from storm.core.di.reflect import Reflect


class Catch:
    """
    Class decorator that marks a class as an exception filter.

    :param exceptions: One or more exception types to catch.
    """

    def __init__(self, *exceptions: Type[Any]):
        self.exceptions = exceptions

    def __call__(self, cls: Type) -> Type:
        Reflect.define_metadata(CATCH_WATERMARK, True, cls)
        Reflect.define_metadata(FILTER_CATCH_EXCEPTIONS, self.exceptions, cls)
        return cls
