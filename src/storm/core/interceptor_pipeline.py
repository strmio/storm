# src/storm/core/interceptor_pipeline.py

import queue


class InterceptorPipeline:
    """
    Manages the sequential execution of global interceptors.

    Attributes:
        - global_interceptors: A list of global interceptors applied to all requests.
    """

    def __init__(self, global_interceptors=None, route_interceptors=None):
        """
        Initializes the InterceptorPipeline with optional global interceptors.

        :param global_interceptors: A list of global interceptor classes.
        :param route_interceptors: A list of route interceptor classes.
        """
        self.global_interceptors = queue.Queue()
        self.route_interceptors = queue.Queue()

        for interceptor in (global_interceptors or []):
            self.global_interceptors.put(interceptor)
        
        for interceptor in (route_interceptors or []):
            self.route_interceptors.put(interceptor)

    def _merge_interceptors(self):
        """Merge global and route interceptors into a single queue."""
        merged_queue = queue.Queue()
        while not self.global_interceptors.empty():
            merged_queue.put(self.global_interceptors.get())
        while not self.route_interceptors.empty():
            merged_queue.put(self.route_interceptors.get())
        return merged_queue

    def add_global_interceptor(self, interceptor_cls):
        """
        Adds a global interceptor to the pipeline.

        :param interceptor_cls: The global interceptor class to be added.
        """
        self.global_interceptors.put(interceptor_cls())

    async def execute(self, request, handler):
        """
        Executes the interceptor pipeline, processing the request through all interceptors.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :return: The response after processing by interceptors and handler.
        """
        all_interceptors = self._merge_interceptors()
        return await self._execute_interceptors(request, handler, all_interceptors)


    async def _execute_interceptors(self, request, handler, interceptor_queue):
        """
        Recursively processes the request through each interceptor in the list.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :param interceptor_queue: The list of interceptors to process the request through.
        :return: The response after processing by interceptors and handler.
        """
        # if not interceptor_list:
        #     return await handler(request)

        # current_interceptor = interceptor_list[0]
        # remaining_interceptors = interceptor_list[1:]

        # async def next_handler(req):
        #     return await self._execute_interceptors(req, handler, remaining_interceptors)

        # return await current_interceptor.intercept(request, next_handler)

        if interceptor_queue.empty():
            return await handler(request)
        
        current_interceptor = interceptor_queue.get()

        async def next_interceptor(req):
            return await self._execute_interceptors(req, handler, interceptor_queue)
        
        return await current_interceptor.intercept(request, next_interceptor)