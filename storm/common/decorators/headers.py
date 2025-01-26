from functools import wraps
from storm.common.execution_context import execution_context


class Headers:
    """
    A unified implementation of Headers that supports async pipes for transformation or validation.

    :param param_name: The name of the parameter to pass to the handler.
    :param header_name: The name of the header to extract from the request.
                        If None, all headers will be passed.
    :param pipe: An optional class or instance of a Pipe to transform or validate the header value(s).
    """

    def __init__(self, param_name=None, header_name=None, pipe=None):
        self.param_name = param_name
        self.header_name = header_name
        self.pipe = pipe

    async def resolve(self):
        """
        Dynamically resolve the header value or all headers, applying the pipe if specified.
        """
        request = execution_context.get_request()
        headers = request.get_headers()

        # Get the specific header or all headers
        if self.header_name is None:
            result = headers
        else:
            result = headers.get(self.header_name)

        # Apply the pipe if it exists
        if self.pipe and result is not None:
            # Instantiate the pipe if it's a class
            pipe_instance = self.pipe() if isinstance(self.pipe, type) else self.pipe
            result = await pipe_instance.transform(
                result, metadata={"header_name": self.header_name}
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
            headers = request.get_headers()

            # Resolve the header value and apply the pipe if necessary
            if self.header_name in headers:
                value = headers[self.header_name]
                if self.pipe:
                    pipe_instance = (
                        self.pipe() if isinstance(self.pipe, type) else self.pipe
                    )
                    value = await pipe_instance.transform(
                        value, metadata={"header_name": self.header_name}
                    )
                kwargs[self.param_name] = value
            else:
                kwargs[self.param_name] = headers

            # Call the original function with updated kwargs
            return await func(*args, **kwargs)

        return wrapper
