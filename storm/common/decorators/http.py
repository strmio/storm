from functools import wraps


def route(method, path=""):
    """Generic decorator to define HTTP routes."""

    def decorator(func):
        # Use wraps to preserve function's metadata
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        version = getattr(func, "version", None)
        # Attach route metadata as attributes
        wrapper.is_route = True
        wrapper._route = {"method": method.upper(), "path": path, "version": version}
        wrapper.route_version = version
        wrapper.route_method = method.upper()
        wrapper.route_path = path

        return wrapper

    return decorator


def Get(path=""):
    """Decorator to define a GET route."""
    return route("GET", path)


def Post(path=""):
    """Decorator to define a POST route."""
    return route("POST", path)


def Put(path=""):
    """Decorator to define a PUT route."""
    return route("PUT", path)


def Delete(path=""):
    """Decorator to define a DELETE route."""
    return route("DELETE", path)


def Patch(path=""):
    """Decorator to define a PATCH route."""
    return route("PATCH", path)


def Options(path=""):
    """Decorator to define a OPTIONS route."""
    return route("OPTIONS", path)


def Head(path=""):
    """Decorator to define a HEAD route."""
    return route("HEAD", path)
