from functools import wraps
from storm.common.execution_context import execution_context

class Body:
    """
    A unified decorator and parameter resolver for request body parameters.
    Can be used as a decorator or directly as a function parameter with an optional pipe.

    :param param_name: The name of the field in the request body to extract. If None, the entire body is used.
    :param pipe: An optional pipe to validate or transform the body parameter value.
    """
    def __init__(self, param_name=None, pipe=None):
        self.param_name = param_name
        self.pipe = pipe

    async def resolve(self):
        """
        Resolve the body parameter from the request, optionally applying a pipe.
        """
        # Get the current request from the execution context
        request = execution_context.get_request()
        body = request.get_body()

        # Get the specific field from the body or use the entire body
        result = body.get(self.param_name) if self.param_name else body

        # Apply the pipe if provided
        if self.pipe and result is not None:
            # Instantiate the pipe if it's a class
            pipe_instance = self.pipe() if isinstance(self.pipe, type) else self.pipe
            result = await pipe_instance.transform(result, metadata={"type": "body", "data": self.param_name})

        return result

    def __call__(self, func=None):
        # If called without a function, resolve the value synchronously for default arguments
        if func is None:
            import asyncio
            return asyncio.run(self.resolve())

        # If called as a decorator
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Resolve the body parameter value
            value = await self.resolve()
            param_name = self.param_name or "body"
            kwargs[param_name] = value

            # Call the original function with the updated kwargs
            return await func(*args, **kwargs)

        return wrapper
