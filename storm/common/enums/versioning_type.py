from enum import IntEnum


class VersioningType(IntEnum):
    URI = 0
    HEADER = 1
    MEDIA_TYPE = 2
    CUSTOM = 3
