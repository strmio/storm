from functools import wraps
from storm.common.execution_context import execution_context

def Host(param_name="host"):
    """
    Decorator to inject the host into the route handler.

    :param param_name: The name of the parameter to pass the host.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            context = execution_context.get()
            request = context.get("request", {})

            # Inject ip 
            kwargs[param_name] = request.get("host", None)

            # Call the original function with the updated kwargs
            return await func(*args, **kwargs)

        return wrapper

    return decorator
