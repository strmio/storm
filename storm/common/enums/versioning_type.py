from enum import StrEnum


class VersioningType(StrEnum):
    URI = "URI"
    HEADER = "HEADER"
    MEDIA_TYPE = "MEDIA_TYPE"
    CUSTOM = "CUSTOM"
