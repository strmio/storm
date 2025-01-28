import queue
from typing import List, Type, Callable, Awaitable, Optional, Any
from storm.common import Interceptor
from storm.core.resolvers.params_resolver import ParamsResolver


class InterceptorPipeline:
    """
    Manages the sequential execution of global and route interceptors.

    Attributes:
        - global_interceptors: A list of global interceptors applied to all requests.
        - route_interceptors: A list of route-specific interceptors.
    """

    def __init__(
        self,
        global_interceptors: Optional[List[Type["Interceptor"]]] = None,
        route_interceptors: Optional[List[Type["Interceptor"]]] = None,
    ):
        """
        Initializes the InterceptorPipeline with optional global and route interceptors.

        :param global_interceptors: A list of global interceptor classes.
        :param route_interceptors: A list of route interceptor classes.
        """
        self.global_interceptors: List["Interceptor"] = []
        self.route_interceptors: List["Interceptor"] = []

        for interceptor in global_interceptors or []:
            self.global_interceptors.append(interceptor())

        for interceptor in route_interceptors or []:
            self.route_interceptors.append(interceptor())

    def add_global_interceptor(self, interceptor_cls: Type["Interceptor"]) -> None:
        """
        Adds a global interceptor to the pipeline.

        :param interceptor_cls: The global interceptor class to be added.
        """
        self.global_interceptors.append(interceptor_cls())

    def _merge_interceptors(self) -> queue.Queue:
        """
        Merges the global and route interceptor lists into a single queue.

        :return: A queue of all interceptors in the pipeline.
        """
        all_interceptors = queue.Queue()
        for interceptor in self.global_interceptors:
            all_interceptors.put(interceptor)
        for interceptor in self.route_interceptors:
            all_interceptors.put(interceptor)
        return all_interceptors

    async def execute(
        self, request: Any, handler: Callable[..., Awaitable[Any]]
    ) -> Any:
        """
        Executes the interceptor pipeline, processing the request through all interceptors.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :return: The response after processing by interceptors and handler.
        """
        all_interceptors = self._merge_interceptors()
        return await self._execute_interceptors(request, handler, all_interceptors)

    async def _execute_interceptors(
        self,
        request: Any,
        handler: Callable[..., Awaitable[Any]],
        interceptor_queue: queue.Queue,
    ) -> Any:
        """
        Recursively processes the request through each interceptor in the list.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :param interceptor_queue: The list of interceptors to process the request through.
        :return: The response after processing by interceptors and handler.
        """
        if interceptor_queue.empty():
            # Resolve arguments for the handler using the Resolver
            resolved_args = await ParamsResolver.resolve(handler, request)
            return await handler(**resolved_args)

        current_interceptor: "Interceptor" = interceptor_queue.get()

        async def next_interceptor(req: Any) -> Any:
            return await self._execute_interceptors(req, handler, interceptor_queue)

        return await current_interceptor.intercept(request, next_interceptor)
