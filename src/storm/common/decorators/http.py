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

def Get(path):
    return route('GET', path)

def Post(path):
    return route('POST', path)

def Put(path):
    return route('PUT', path)

def Delete(path):
    return route('DELETE', path)
