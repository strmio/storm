from enum import StrEnum

class SessionType(StrEnum):
    COOKIE = "cookie"
    TOKEN = "token"
    JWT = "jwt"
    OAUTH2 = "oauth2"
    LOCAL = "local"
