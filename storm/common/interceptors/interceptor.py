from typing import Callable, Awaitable, Any
from storm.common.execution_context import ExecutionContext


class Interceptor:
    """
    Base class for all interceptors. Interceptors can transform the execution context before
    it reaches the controller and transform the response after the controller processes the context.
    """

    async def intercept(
        self,
        context: ExecutionContext,
        next: Callable[[ExecutionContext], Awaitable[Any]],
    ) -> Any:
        """
        Process the execution context and optionally transform the response.

        :param context: The execution context for the current request.
        :param next: A function to call the next interceptor or controller action.
        :return: The response after processing.
        """
        return await next()
