from functools import wraps

from storm.core.router import Router

routes = Router()

def route(method, path):
    """
    A decorator that registers a route with a specific HTTP method and path.

    :param method: The HTTP method (GET, POST, etc.)
    :param path: The URL path (e.g., '/users/:id')
    :return: The decorated function
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        routes.add_route(method, path, wrapper)  # Add the route to the router instance
        return wrapper
    return decorator

def get(path):
    return route('GET', path)

def post(path):
    return route('POST', path)

def put(path):
    return route('PUT', path)

def delete(path):
    return route('DELETE', path)
