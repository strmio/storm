from enum import Enum

class CORSSetting(Enum):
    ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    ALLOW_METHODS = "Access-Control-Allow-Methods"
    ALLOW_HEADERS = "Access-Control-Allow-Headers"
    ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
    EXPOSE_HEADERS = "Access-Control-Expose-Headers"
    MAX_AGE = "Access-Control-Max-Age"
