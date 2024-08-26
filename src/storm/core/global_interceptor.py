# src/storm/core/global_interceptor.py

from abc import ABC, abstractmethod

class GlobalInterceptor(ABC):
    """
    Abstract base class for global interceptors in the Storm framework.

    Global interceptors can inspect and modify incoming requests before they reach the controller
    and can also modify outgoing responses after they have been processed by the controller.
    """

    @abstractmethod
    async def intercept(self, request, next_handler):
        """
        Intercept the incoming request and/or outgoing response.

        :param request: The incoming request object
        :param next_handler: The next function or middleware in the chain
        :return: The response after processing by the next handler
        """
        pass
