from functools import wraps
from storm.core.router import Router

router = Router()

def route(method, path):
    """
    A decorator that registers a route with a specific HTTP method and path.

    :param method: The HTTP method (GET, POST, etc.)
    :param path: The URL path (e.g., '/users/:id')
    :return: The decorated function with routing metadata
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            """
            The actual function wrapper that gets executed.

            :param args: Positional arguments
            :param kwargs: Keyword arguments, including request-specific data
            :return: The result of the function execution
            """
            return await func(*args, **kwargs)
        router.add_route(method, path, wrapper)
        return wrapper
    return decorator
