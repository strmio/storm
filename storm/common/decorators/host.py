from functools import wraps

from storm.common.execution_context import ExecutionContext


def Host(param_name="host"):
    """
    Decorator to inject the host into the route handler.

    :param param_name: The name of the parameter to pass the host.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            request = ExecutionContext.get_request()
            if request is None:
                raise ValueError("No request found in the execution context")
            host = request.get_server_host()

            # Inject ip
            kwargs[param_name] = host

            # Call the original function with the updated kwargs
            return await func(*args, **kwargs)

        return wrapper

    return decorator
