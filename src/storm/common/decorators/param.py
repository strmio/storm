from functools import wraps
from storm.common.execution_context import execution_context

def Param(param_name = "params"):
    """
    Decorator to inject a specific route parameter into the handler.

    :param param_name: The name of the route parameter to inject.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            context = execution_context.get()
            route_params = context.get("request", {}).get("params", {})

            # Inject the route parameter into kwargs if it exists
            if param_name in route_params:
                kwargs[param_name] = route_params[param_name]
            else:
                kwargs[param_name] = route_params

            # Call the original function with updated kwargs
            return await func(*args, **kwargs)

        return wrapper

    return decorator


class Params:
    """
    A placeholder for route parameters to be resolved dynamically.
    If param_name is None, all route parameters will be returned.
    """
    def __init__(self, param_name=None):
        self.param_name = param_name

    def resolve(self):
        """
        Dynamically resolve the parameter value or all parameters.
        """
        context = execution_context.get()
        route_params = context.get("request", {}).get("params", {})

        if self.param_name is None:
            return route_params
        return route_params.get(self.param_name)
