# storm/common/decorators/http/request_mapping.py

from typing import Callable, List, Optional, Union

from storm.common.constants import METHOD_METADATA, PATH_METADATA
from storm.common.enums.request_method import RequestMethod
from storm.core.di.reflect import Reflect


class RequestMappingMetadata:
    """
    Represents metadata for an HTTP route mapping.
    """

    def __init__(
        self,
        path: Union[str, List[str]] = "/",
        method: RequestMethod = RequestMethod.GET,
    ):
        self.path = path or "/"
        self.method = method


class RequestMapping:
    """
    Decorator that applies HTTP route metadata to a handler function.
    """

    def __init__(self, metadata: RequestMappingMetadata):
        self.metadata = metadata

    def __call__(self, target: object, key: str | None = None, descriptor: Callable | None = None):
        """
        Assigns path and method metadata to the decorated method.

        :param target: The class prototype or function
        :param key: The method name (only for method decorators)
        :param descriptor: The method (function) object to decorate
        """
        if callable(target):
            # Function/class decorator
            Reflect.define_metadata(PATH_METADATA, self.metadata.path, target)
            Reflect.define_metadata(METHOD_METADATA, self.metadata.method, target)
            return target

        if descriptor is not None:
            Reflect.define_metadata(PATH_METADATA, self.metadata.path, descriptor)
            Reflect.define_metadata(METHOD_METADATA, self.metadata.method, descriptor)
            return descriptor

        raise TypeError("@RequestMapping must be used on a method or function")


def create_mapping_decorator(method: RequestMethod) -> Callable[[Optional[Union[str, list[str]]]], Callable]:
    """
    Factory function to create route method decorators.

    :param method: HTTP method (GET, POST, etc.) to associate with the handler.
    :return: A decorator that sets metadata for path and method on the route handler.
    """

    def decorator(path: Optional[Union[str, list[str]]] = "/") -> Callable:
        return RequestMapping(RequestMappingMetadata(path=path or "/", method=method))

    return decorator


# Standard HTTP decorators
Get = create_mapping_decorator(RequestMethod.GET)
Post = create_mapping_decorator(RequestMethod.POST)
Put = create_mapping_decorator(RequestMethod.PUT)
Delete = create_mapping_decorator(RequestMethod.DELETE)
Patch = create_mapping_decorator(RequestMethod.PATCH)
Options = create_mapping_decorator(RequestMethod.OPTIONS)
Head = create_mapping_decorator(RequestMethod.HEAD)
All = create_mapping_decorator(RequestMethod.ALL)

# WebDAV decorators
Search = create_mapping_decorator(RequestMethod.SEARCH)
Propfind = create_mapping_decorator(RequestMethod.PROPFIND)
Proppatch = create_mapping_decorator(RequestMethod.PROPPATCH)
Mkcol = create_mapping_decorator(RequestMethod.MKCOL)
Copy = create_mapping_decorator(RequestMethod.COPY)
Move = create_mapping_decorator(RequestMethod.MOVE)
Lock = create_mapping_decorator(RequestMethod.LOCK)
Unlock = create_mapping_decorator(RequestMethod.UNLOCK)
