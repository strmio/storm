from functools import wraps


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

        return wrapper

    return decorator
