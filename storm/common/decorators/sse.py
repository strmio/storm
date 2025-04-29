from functools import wraps

from storm.common.constants import SSE_METADATA
from storm.core.reflector import Reflector


def Sse(path=""):
    """Decorator to define an SSE (Server-Sent Events) GET route."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Attach route metadata
        wrapper.is_route = True
        wrapper._route = {"method": "GET", "path": path}
        wrapper.route_method = "GET"
        wrapper.route_path = path
        wrapper.is_sse = True  # Mark it as an SSE route
        Reflector.set_watermark(wrapper, SSE_METADATA)
        Reflector.set_metadata(wrapper, "is_sse", True)
        Reflector.set_metadata(wrapper, "path", path)
        Reflector.set_metadata(wrapper, "method", "GET")

        return wrapper

    return decorator
