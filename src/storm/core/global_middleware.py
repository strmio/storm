from abc import ABC, abstractmethod

class GlobalMiddleware(ABC):
    """
    Abstract base class for global middleware in the Storm framework.

    Global middleware are applied to all routes and controllers within the application.
    Subclasses should implement the `process` method to define custom logic.
    """

    @abstractmethod
    async def process_request(self, request, next_handler):
        """
        Process the incoming request and optionally modify it.

        :param request: The incoming request object
        :param next_handler: The next middleware or handler in the pipeline
        :return: The response from the next middleware or handler
        """
        pass
