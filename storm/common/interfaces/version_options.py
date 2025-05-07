from typing import Callable, List, Optional, Union

from storm.common import VersioningType

VersionValue = Union[str, object, List[Union[str, object]]]  # object = VERSION_NEUTRAL


class VersionOptions:
    def __init__(self, version: Optional[VersionValue] = None):
        self.version = version


class HeaderVersioningOptions:
    def __init__(self, header: str):
        self.type = VersioningType.HEADER
        self.header = header


class UriVersioningOptions:
    def __init__(self, prefix: Optional[Union[str, bool]] = "v"):
        self.type = VersioningType.URI
        self.prefix = prefix


class MediaTypeVersioningOptions:
    def __init__(self, key: str):
        self.type = VersioningType.MEDIA_TYPE
        self.key = key


class CustomVersioningOptions:
    def __init__(self, extractor: Callable[[object], Union[str, List[str]]]):
        self.type = VersioningType.CUSTOM
        self.extractor = extractor


class VersioningOptions:
    def __init__(
        self,
        default_version: Optional[VersionValue] = None,
        strategy: Union[HeaderVersioningOptions, UriVersioningOptions, MediaTypeVersioningOptions, CustomVersioningOptions, None] = None,
    ):
        self.default_version = default_version
        self.strategy = strategy
