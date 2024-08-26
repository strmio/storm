# src/storm/core/middleware_pipeline.py

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
        self.global_middleware = global_middleware or []
        self.route_middleware = route_middleware or []

    def add_global_middleware(self, middleware_cls):
        """
        Adds a global middleware to the pipeline.

        :param middleware_cls: The global middleware class to be added.
        """
        self.global_middleware.append(middleware_cls())

    async def execute(self, request, handler):
        """
        Executes the middleware pipeline, processing the request through all middleware.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :return: The response after processing by middleware and handler.
        """
        all_middleware = self.global_middleware + self.route_middleware
        if not all_middleware:
            return request
        return await self._execute_request_middleware(request, handler, all_middleware)

    async def _execute_request_middleware(self, request, handler, middleware_list):
        """
        Recursively processes the request through each middleware in the list.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :param middleware_list: The list of middleware to process the request through.
        :return: The response after processing by middleware and handler.
        """
        if not middleware_list:
            return handler(request)

        current_middleware = middleware_list[0]
        remaining_middleware = middleware_list[1:]

        async def next_handler(req):
            return await self._execute_request_middleware(req, handler, remaining_middleware)

        if hasattr(current_middleware, 'process'):
            return await current_middleware.process(request, next_handler)
        return await current_middleware.process_request(request, next_handler)
