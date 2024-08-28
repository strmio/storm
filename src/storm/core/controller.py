# src/storm/core/controller.py

class ControllerBase:
    def __init__(self, middleware=[]):
        self.middleware = middleware

    async def execute(self, request):
        async def next_middleware(index):
            if index < len(self.middleware):
                middleware = self.middleware[index]
                return await middleware.handle(request, lambda: next_middleware(index + 1))
            else:
                return await self.action(request)  # Assuming 'action' is the controller's method.

        return await next_middleware(0)
