from functools import wraps
from storm.common.execution_context import execution_context

class Param:
    """
    A unified implementation of Param/Params that can work both as a decorator
    and as a dynamic parameter resolver in function arguments.

    :param param_name: The name of the route parameter to inject or resolve.
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

    def __call__(self, func=None):
        # If called without a function, act as a resolver
        if func is None:
            return self.resolve()

        # If called with a function, act as a decorator
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            context = execution_context.get()
            route_params = context.get("request", {}).get("params", {})

            # Inject the route parameter into kwargs if it exists
            if self.param_name in route_params:
                kwargs[self.param_name] = route_params[self.param_name]
            else:
                kwargs[self.param_name] = route_params

            # Call the original function with updated kwargs
            return await func(*args, **kwargs)

        return wrapper
