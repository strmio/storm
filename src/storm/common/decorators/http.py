from functools import wraps

routes = {}

def route(method, path):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        routes[(method, path)] = func
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
