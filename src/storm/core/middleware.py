class Middleware:
    """
    Base class for middleware. Middleware classes should extend this class and implement the `handle` method.
    """
    async def handle(self, request, next):
        """
        Process the request and pass it to the next middleware or controller.
        :param request: The incoming request object.
        :param next: A function to call the next middleware or controller.
        :return: The response after processing.
        """
        raise NotImplementedError("Middleware must implement the handle method.")
