from functools import wraps

from storm.common.execution_context import ExecutionContext


def Ip(param_name="ip"):
    """
    Decorator to inject the client's IP address into the route handler.

    :param param_name: The name of the parameter to pass the IP address.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            request = ExecutionContext.get_request()
            if request is None:
                raise ValueError("No request object found in execution context")
            ip = request.get_client_ip()

            # Inject ip
            kwargs[param_name] = ip

            # Call the original function with the updated kwargs
            return await func(*args, **kwargs)

        return wrapper

    return decorator
