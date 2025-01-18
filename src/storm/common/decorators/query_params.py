from functools import wraps
from storm.common.execution_context import execution_context

def Query(param_name, query_param_name=None):
    """
    Decorator to inject a specific query parameter or all query parameters
    into the route handler as a parameter.

    :param param_name: The name of the parameter to pass to the handler.
    :param query_param_name: The name of the query parameter to extract from the request.
                             If None, all query parameters will be passed.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            context = execution_context.get()
            request = context.get("request", {})
            query_params = request.get("query_params", {})

            if query_param_name:
                # Inject the specific query parameter
                kwargs[param_name] = query_params.get(query_param_name)
            else:
                # Inject all query parameters
                kwargs[param_name] = query_params

            # Call the original function with the updated kwargs
            return await func(*args, **kwargs)

        return wrapper

    return decorator
