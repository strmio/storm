from storm.core.middleware import Middleware

class LoggerMiddleware(Middleware):
    async def handle(self, request, next):
        print(f"Handling request: {request.path}")
        response = await next()  # Call the next middleware or controller
        print(f"Finished handling request: {request.path}")
        return response
