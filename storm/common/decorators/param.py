from functools import wraps
from storm.common.execution_context import execution_context


class Param:
    """
    A unified implementation of Param that supports async pipes for transformation or validation.

    :param param_name: The name of the route parameter to inject or resolve.
    :param pipe: An optional class or instance of a Pipe to transform or validate the parameter.
    """

    def __init__(self, param_name=None, pipe=None):
        self.param_name = param_name
        self.pipe = pipe

    async def resolve(self):
        """
        Dynamically resolve the parameter value or all parameters, applying the pipe if specified.
        """
        request = execution_context.get_request()
        route_params = request.get_params()

        # Get the parameter value or all parameters
        if self.param_name is None:
            result = route_params
        else:
            result = route_params.get(self.param_name)

        # Apply the pipe if it exists
        if self.pipe and result is not None:
            # Instantiate the pipe if it's a class
            pipe_instance = self.pipe() if isinstance(self.pipe, type) else self.pipe
            result = await pipe_instance.transform(
                result, metadata={"param_name": self.param_name}
            )
        return result

    def __call__(self, func=None):
        # If called without a function, resolve the value synchronously for default arguments
        if func is None:
            import asyncio

            return asyncio.run(self.resolve())

        # If called with a function, act as a decorator
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            request = execution_context.get_request()
            route_params = request.get_params()

            # Resolve the parameter value and apply the pipe if necessary
            if self.param_name in route_params:
                value = route_params[self.param_name]
                if self.pipe:
                    pipe_instance = (
                        self.pipe() if isinstance(self.pipe, type) else self.pipe
                    )
                    value = await pipe_instance.transform(
                        value, metadata={"param_name": self.param_name}
                    )
                kwargs[self.param_name] = value
            else:
                kwargs[self.param_name] = route_params

            # Call the original function with updated kwargs
            return await func(*args, **kwargs)

        return wrapper
