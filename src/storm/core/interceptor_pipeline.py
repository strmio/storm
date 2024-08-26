# src/storm/core/interceptor_pipeline.py

class InterceptorPipeline:
    """
    Manages the sequential execution of global interceptors.

    Attributes:
        - global_interceptors: A list of global interceptors applied to all requests.
    """

    def __init__(self, global_interceptors=None):
        """
        Initializes the InterceptorPipeline with optional global interceptors.

        :param global_interceptors: A list of global interceptor classes.
        """
        self.global_interceptors = global_interceptors or []

    def add_global_interceptor(self, interceptor_cls):
        """
        Adds a global interceptor to the pipeline.

        :param interceptor_cls: The global interceptor class to be added.
        """
        self.global_interceptors.append(interceptor_cls())

    async def execute(self, request, handler):
        """
        Executes the interceptor pipeline, processing the request through all interceptors.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :return: The response after processing by interceptors and handler.
        """
        return await self._execute_interceptors(request, handler, self.global_interceptors)

    async def _execute_interceptors(self, request, handler, interceptor_list):
        """
        Recursively processes the request through each interceptor in the list.

        :param request: The incoming request object.
        :param handler: The final handler function to process the request.
        :param interceptor_list: The list of interceptors to process the request through.
        :return: The response after processing by interceptors and handler.
        """
        if not interceptor_list:
            return await handler(request)

        current_interceptor = interceptor_list[0]
        remaining_interceptors = interceptor_list[1:]

        async def next_handler(req):
            return await self._execute_interceptors(req, handler, remaining_interceptors)

        return await current_interceptor.intercept(request, next_handler)
