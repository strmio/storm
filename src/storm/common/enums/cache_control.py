from enum import Enum

class CacheControl(Enum):
    NO_CACHE = "no-cache"
    NO_STORE = "no-store"
    MUST_REVALIDATE = "must-revalidate"
    PUBLIC = "public"
    PRIVATE = "private"
    MAX_AGE = "max-age"
    S_MAXAGE = "s-maxage"
    NO_TRANSFORM = "no-transform"
    IMMUTABLE = "immutable"
    STALE_WHILE_REVALIDATE = "stale-while-revalidate"
