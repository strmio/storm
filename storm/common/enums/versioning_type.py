from enum import IntEnum


class VersioningType(IntEnum):
    URI = "URI"
    HEADER = "HEADER"
    MEDIA_TYPE = "MEDIA_TYPE"
    CUSTOM = "CUSTOM"
