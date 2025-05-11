from enum import StrEnum


class RequestMethod(StrEnum):
    # Standard HTTP methods
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    ALL = "ALL"

    # WebDAV methods
    PROPFIND = "PROPFIND"
    PROPPATCH = "PROPPATCH"
    MKCOL = "MKCOL"
    COPY = "COPY"
    MOVE = "MOVE"
    LOCK = "LOCK"
    UNLOCK = "UNLOCK"

    # Additional methods
    SEARCH = "SEARCH"
    TRACE = "TRACE"
    CONNECT = "CONNECT"
