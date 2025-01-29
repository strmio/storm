import queue
from rx import Observable
from typing import List, Type, Callable, Awaitable, Optional, Any, Union
from storm.common import Interceptor
from storm.common.execution_context import ExecutionContext, execution_context
from storm.core.resolvers.params_resolver import ParamsResolver
import inspect


class InterceptorPipeline:
    """
    Manages the sequential execution of global and route interceptors.
    """

    def __init__(
        self,
        global_interceptors: Optional[
            List[Union[Type[Interceptor], Interceptor]]
        ] = None,
        route_interceptors: Optional[
            List[Union[Type[Interceptor], Interceptor]]
        ] = None,
    ):
        """
        Initializes the InterceptorPipeline with optional global and route interceptors.

        :param global_interceptors: A list of global interceptor classes or instances.
        :param route_interceptors: A list of route interceptor classes or instances.
        """
        self.global_interceptors: List[Interceptor] = []
        self.route_interceptors: List[Interceptor] = []

        for interceptor in global_interceptors or []:
            self.add_global_interceptor(interceptor)

        for interceptor in route_interceptors or []:
            self.add_route_interceptor(interceptor)

    def add_global_interceptor(
        self, interceptor: Union[Type[Interceptor], Interceptor]
    ) -> None:
        """
        Adds a global interceptor to the pipeline.

        :param interceptor: The global interceptor class or instance to be added.
        """
        if isinstance(interceptor, type) and issubclass(interceptor, Interceptor):
            self.global_interceptors.append(interceptor())
        elif isinstance(interceptor, Interceptor):
            self.global_interceptors.append(interceptor)
        else:
            raise TypeError("interceptor must be a subclass or instance of Interceptor")

    def add_route_interceptor(
        self, interceptor: Union[Type[Interceptor], Interceptor]
    ) -> None:
        """
        Adds a route interceptor to the pipeline.

        :param interceptor: The route interceptor class or instance to be added.
        """
        if isinstance(interceptor, type) and issubclass(interceptor, Interceptor):
            self.route_interceptors.append(interceptor())
        elif isinstance(interceptor, Interceptor):
            self.route_interceptors.append(interceptor)
        else:
            raise TypeError("interceptor must be a subclass or instance of Interceptor")

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

    async def execute(self, handler: Callable[..., Awaitable[Any]]) -> Any:
        """
        Executes the interceptor pipeline, processing the context through all interceptors.

        :param handler: The final handler function to process the context.
        :return: The response after processing by interceptors and handler.
        """
        all_interceptors = self._merge_interceptors()
        return await self._execute_interceptors(handler, all_interceptors)

    async def _execute_interceptors(
        self, handler: Callable[..., Awaitable[Any]], interceptor_queue: queue.Queue
    ) -> Any:
        """
        Recursively processes the context through each interceptor in the list.

        :param handler: The final handler function.
        :param interceptor_queue: The queue of interceptors to process the context through.
        :return: The response after processing by interceptors and handler.
        """
        if interceptor_queue.empty():
            # Resolve arguments for the handler using the Resolver
            resolved_args = await ParamsResolver.resolve(
                handler, execution_context.get_request()
            )
            response = await handler(**resolved_args)
            if isinstance(response, Observable):
                return await self._execute_observable(response)
            return await handler(**resolved_args)

        current_interceptor: Interceptor = interceptor_queue.get()

        async def next_interceptor():
            return await self._execute_interceptors(handler, interceptor_queue)

        return await self._call_interceptor(current_interceptor, next_interceptor)

    async def _call_interceptor(
        self, interceptor: Interceptor, next_interceptor: Callable[[], Awaitable[Any]]
    ) -> Any:
        """
        Dynamically injects dependencies and calls the interceptor's `intercept` method.

        :param interceptor: The current interceptor instance.
        :param next_interceptor: The next interceptor or handler to be called.
        :return: The response after processing by the current interceptor.
        """
        intercept_method = interceptor.intercept
        signature = inspect.signature(intercept_method)
        kwargs = {}

        for param_name, param in signature.parameters.items():
            if param_name == "next":
                kwargs[param_name] = next_interceptor
            elif param.annotation is ExecutionContext:
                kwargs[param_name] = execution_context

        return await intercept_method(**kwargs)

    async def _execute_observable(self, observable: Observable) -> Any:
        """
        Executes an observable returned from the handler and collects the results.

        :param observable: An instance of rx.Observable.
        :return: The result emitted by the observable.
        """
        result = None

        def on_next(value):
            nonlocal result
            result = value  # Capture the emitted value

        def on_error(error):
            raise Exception(f"Observable error: {error}")

        def on_completed():
            pass  # Do nothing on completion

        # Subscribe to the observable and block until it's done
        observable.subscribe(
            on_next=on_next,
            on_error=on_error,
            on_completed=on_completed,
        )

        return result
