# storm/common/decorators/http/sse.py

from typing import Callable, Optional

from storm.common.constants import METHOD_METADATA, PATH_METADATA, SSE_METADATA
from storm.common.enums.request_method import RequestMethod
from storm.core.di.reflect import Reflect


class Sse:
    """
    Decorator that marks a method as a Server-Sent Events (SSE) endpoint.

    :param path: Optional path for the route. Defaults to "/".
    """

    def __init__(self, path: Optional[str] = None):
        self.path = path if path else "/"

    def __call__(self, func: Callable) -> Callable:
        Reflect.define_metadata(PATH_METADATA, self.path, func)
        Reflect.define_metadata(METHOD_METADATA, RequestMethod.GET, func)
        Reflect.define_metadata(SSE_METADATA, True, func)
        return func
