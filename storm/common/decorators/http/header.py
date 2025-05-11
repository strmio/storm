# storm/common/decorators/http/header.py

from typing import Callable, Union

from storm.common.constants import HEADERS_METADATA
from storm.common.utils.extend_metadata import extend_array_metadata


class Header:
    """
    Method decorator to set response headers.

    Example:
        @Header("Cache-Control", "none")
        @Header("Cache-Control", lambda: "no-cache")
    """

    def __init__(self, name: str, value: Union[str, Callable[[], str]]):
        self.name = name
        self.value = value

    def __call__(self, func):
        extend_array_metadata(HEADERS_METADATA, [{"name": self.name, "value": self.value}], func)
        return func
