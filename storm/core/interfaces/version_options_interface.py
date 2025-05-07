from typing import Callable, Dict, List, Optional, Protocol, Type, Union

from storm.common.enums.versioning_type import VersioningType


class _VersionNeutral:
    def __repr__(self):
        return "VERSION_NEUTRAL"


VERSION_NEUTRAL = _VersionNeutral()

VersionValue = Union[str, _VersionNeutral, List[Union[str, _VersionNeutral]]]


class VersionOptions(Protocol):
    version: Optional[VersionValue]


class HeaderVersioningOptions:
    """
    Represents versioning options for header-based versioning.

    Attributes:
        type (VersioningType): The type of versioning, which is set to HEADER.
        header (str): The name of the header used for versioning.

    Methods:
        __init__(header: str):
            Initializes the HeaderVersioningOptions with the specified header name.
    """

    type: VersioningType
    header: str

    def __init__(self, header: str):
        self.type = VersioningType.HEADER
        self.header = header


class UriVersioningOptions:
    """
    Represents versioning options for URI-based versioning.

    Attributes:
        type (VersioningType): The type of versioning, which is set to URI.
        prefix (Union[str, bool]): The prefix used for versioning in the URI.
            Defaults to 'v'. Can be a string (e.g., 'v1') or a boolean to
            indicate whether a prefix is used.

    Methods:
        __init__(prefix: Union[str, bool] = 'v'):
            Initializes the UriVersioningOptions with the specified prefix.
    """

    type: VersioningType
    prefix: Union[str, bool]

    def __init__(self, prefix: Union[str, bool] = "v"):
        self.type = VersioningType.URI
        self.prefix = prefix


class MediaTypeVersioningOptions:
    """
    Represents versioning options for media type versioning.

    Attributes:
        type (VersioningType): The type of versioning, set to MEDIA_TYPE.
        key (str): The key used for media type versioning.

    Methods:
        __init__(key: str):
            Initializes the MediaTypeVersioningOptions with the specified key.
    """

    type: VersioningType
    key: str

    def __init__(self, key: str):
        self.type = VersioningType.MEDIA_TYPE
        self.key = key


class CustomVersioningOptions:
    """
    A class representing custom versioning options for an object.

    Attributes:
        type (VersioningType): The type of versioning, set to `VersioningType.CUSTOM`.
        extractor (Callable[[object], Union[str, List[str]]]): A callable function that extracts
            version information from an object. The function should return either a string
            or a list of strings representing the version(s).

    Methods:
        __init__(extractor: Callable[[object], Union[str, List[str]]]):
            Initializes the CustomVersioningOptions with a custom extractor function.
    """

    type: VersioningType
    extractor: Callable[[object], Union[str, List[str]]]

    def __init__(self, extractor: Callable[[object], Union[str, List[str]]]):
        self.type = VersioningType.CUSTOM
        self.extractor = extractor


class VersioningCommonOptions(Protocol):
    default_version: Optional[VersionValue]


VersioningOptions = Union[
    HeaderVersioningOptions,
    UriVersioningOptions,
    MediaTypeVersioningOptions,
    CustomVersioningOptions,
]

VERSIONING_CLASS_MAP: Dict[VersioningType, Type[VersioningOptions]] = {
    VersioningType.HEADER: HeaderVersioningOptions,
    VersioningType.URI: UriVersioningOptions,
    VersioningType.MEDIA_TYPE: MediaTypeVersioningOptions,
    VersioningType.CUSTOM: CustomVersioningOptions,
}
