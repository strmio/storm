# src/storm/core/controller.py

from storm.core.router.router import Router


class ControllerBase:
    def __init__(self, base_path="", middleware=[]):
        base_path = base_path
        self.middleware = middleware
        self.router = Router()

    async def execute(self, request):
        async def next_middleware(index):
            if index < len(self.middleware):
                middleware = self.middleware[index]
                return await middleware.handle(
                    request, lambda: next_middleware(index + 1)
                )
            else:
                return await self.action(
                    request
                )  # Assuming 'action' is the controller's method.

        return await next_middleware(0)
