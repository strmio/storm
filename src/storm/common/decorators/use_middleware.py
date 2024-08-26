from functools import wraps


def use_middleware(middleware_list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for middleware in middleware_list:
                await middleware.process_request(args, kwargs)
            response = await func(*args, **kwargs)
            for middleware in middleware_list:
                await middleware.process_response(response)
            return response
        return wrapper
    return decorator
