from enum import Enum

class SessionType(Enum):
    COOKIE = "cookie"
    TOKEN = "token"
    JWT = "jwt"
    OAUTH2 = "oauth2"
    LOCAL = "local"
