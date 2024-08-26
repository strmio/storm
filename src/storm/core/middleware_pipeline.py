# src/storm/core/middleware_pipeline.py

class MiddlewarePipeline:
    """
    Manages the sequential execution of middleware, including global middleware.

    Attributes:
        - global_middleware: A list of global middleware applied to all requests.
        - route_middleware: A list of route-specific middleware.
    """

    def __init__(self, global_middleware=None, route_middleware=None):
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
        Executes the request through the middleware pipeline, including global middleware.

        :param request: The incoming request object
        :param handler: The handler function to process the request
        :return: The response after processing by middleware and handler
        """
        # Combine global middleware with route-specific middleware
        all_middleware = self.global_middleware + self.route_middleware
        return await self._execute_request_middleware(request, handler, all_middleware)

    async def _execute_request_middleware(self, request, handler, middleware_list):
        if not middleware_list:
            return await handler(request)

        current_middleware = middleware_list[0]
        remaining_middleware = middleware_list[1:]

        async def next_handler(req):
            return await self._execute_request_middleware(req, handler, remaining_middleware)
        
        if hasattr(current_middleware, 'process'):
            return await current_middleware.process(request, next_handler)
        return await current_middleware.process_request(request, next_handler)
