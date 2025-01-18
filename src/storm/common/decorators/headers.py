from functools import wraps
from storm.common.execution_context import execution_context

def Header(param_name, header_name=None):
    """
    Decorator to inject a specific header or all headers
    into the route handler as a parameter.

    :param param_name: The name of the parameter to pass to the handler.
    :param header_name: The name of the header to extract from the request.
                        If None, all headers will be passed.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            context = execution_context.get()
            request = context.get("request", {})
            headers = request.get("headers", {})

            if header_name:
                # Inject the specific header
                kwargs[param_name] = headers.get(header_name)
            else:
                # Inject all headers
                kwargs[param_name] = headers

            # Call the original function with the updated kwargs
            return await func(*args, **kwargs)

        return wrapper

    return decorator
