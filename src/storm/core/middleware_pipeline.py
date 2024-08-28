# src/storm/core/middleware_pipeline.py

import queue


class MiddlewarePipeline:
    """
    Manages the sequential execution of middleware, including global and route-specific middleware.

    Attributes:
        - global_middleware: A list of global middleware applied to all requests.
        - route_middleware: A list of middleware specific to certain routes.
    """

    def __init__(self, global_middleware=None, route_middleware=None):
        """
        Initializes the MiddlewarePipeline with optional global and route-specific middleware.

        :param global_middleware: A list of global middleware classes.
        :param route_middleware: A list of route-specific middleware classes.
        """
        self.global_middleware = queue.Queue()
        self.route_middleware = queue.Queue()

        for middleware in (global_middleware or []):
            self.global_middleware.put(middleware)

        for middleware in (route_middleware or []):
            self.route_middleware.put(middleware)

    def _merge_middleware(self):
        """Merge global and route middleware into a single queue."""
        merged_queue = queue.Queue()
        while not self.global_middleware.empty():
            merged_queue.put(self.global_middleware.get())
        while not self.route_middleware.empty():
            merged_queue.put(self.route_middleware.get())
        return merged_queue

    def add_global_middleware(self, middleware_cls):
        """
        Adds a global middleware to the pipeline.

        :param middleware_cls: The global middleware class to be added.
        """
        self.global_middleware.put(middleware_cls())

    async def execute(self, request, handler):
        """
        Executes the middleware pipeline, processing the request through all middleware.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :return: The response after processing by middleware and handler.
        """
        all_middleware = self._merge_middleware()
        if all_middleware.empty():
            return request
        return await self._execute_request_middleware(request, handler, all_middleware)

    async def _execute_request_middleware(self, request, handler, middleware_queue):
        """
        Recursively processes the request through each middleware in the list.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :param middleware_list: The list of middleware to process the request through.
        :return: The response after processing by middleware and handler.
        """

        if middleware_queue.empty():
            return handler(request)

        current_middleware = middleware_queue.get()

        async def next_middleware(req):
            return await self._execute_request_middleware(req, handler, middleware_queue)

        return await current_middleware.process_request(request, next_middleware)
