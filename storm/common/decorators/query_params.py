from functools import wraps

from storm.common.execution_context import execution_context


class Query:
    """
    A unified decorator and parameter resolver for query parameters.
    Can be used as a decorator or directly as a function parameter with an optional pipe.

    :param query_param_name: The name of the query parameter to extract from the request.
                             If None, all query parameters will be passed.
    :param pipe: An optional pipe to validate or transform the query parameter value.
    """

    def __init__(self, query_param_name=None, param_name=None, pipe=None):
        self.param_name = param_name
        self.query_param_name = query_param_name
        self.pipe = pipe

    async def resolve(self):
        """
        Resolve the query parameter from the request, optionally applying a pipe.
        """
        # Get the current request from the execution context
        request = execution_context.get_request()
        query_params = request.get_query_params()

        # Get the specific query parameter or all query parameters
        if self.query_param_name:
            result = query_params.get(self.query_param_name)
        else:
            result = query_params

        # Apply the pipe if provided
        if self.pipe and result is not None:
            # Instantiate the pipe if it's a class
            pipe_instance = self.pipe() if isinstance(self.pipe, type) else self.pipe
            result = await pipe_instance.transform(result, metadata={"type": "query", "data": self.query_param_name})

        return result

    def __call__(self, func=None):
        # If called without a function, resolve the value synchronously for default arguments
        if func is None:
            import asyncio

            return asyncio.run(self.resolve())

        # If called as a decorator
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Resolve the query parameter value
            value = await self.resolve()
            param_name = self.query_param_name or "query_params"
            kwargs[param_name] = value

            # Call the original function with the updated kwargs
            return await func(*args, **kwargs)

        return wrapper
