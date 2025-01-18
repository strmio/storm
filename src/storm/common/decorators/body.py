from functools import wraps
from storm.common.execution_context import execution_context

def Body(param_name):
    """
    Decorator to inject the current request from the execution context
    as a parameter to the route handler.

    :param param_name: The name of the parameter to inject the request into.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            context = execution_context.get()
            request = context.get("request", None)
            body = request.get("body", None)
            # Inject the request into the kwargs using the given param_name
            if body:
                kwargs[param_name] = body

            # Call the original function with the updated kwargs
            return await func(*args, **kwargs)

        return wrapper

    return decorator
