from functools import wraps

from storm.common.execution_context import ExecutionContext


def Request(param_name):
    """
    Decorator to inject the current request from the execution context
    as a parameter to the route handler.

    :param param_name: The name of the parameter to inject the request into.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            request = ExecutionContext.get_request()

            # Inject the request into the kwargs using the given param_name
            if request:
                kwargs[param_name] = request

            # Call the original function with the updated kwargs
            return await func(*args, **kwargs)

        return wrapper

    return decorator


# Alias for Request to allow it to be imported as Req or Request
Req = Request
