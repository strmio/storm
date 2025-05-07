from modules.app_module import AppModule

from storm.common import ExecutionContext, Interceptor, Logger
from storm.core import StormApplication

# Initialize the application with AppModule
app = StormApplication(AppModule)


class GlobalLogInterceptor(Interceptor):
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    async def intercept(self, ctx: ExecutionContext, next):
        """
        Process the request and optionally transform the response.
        :param request: The incoming request object.
        :param next: A function to call the next interceptor or controller action.
        :return: The response after processing.
        """
        self.logger.info(f"Logging Request {ctx.get_request()}")
        res = await next()
        self.logger.info(f"Logging Response {res}")
        return res


class ResHeadersInterceptor(Interceptor):
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    async def intercept(self, ctx: ExecutionContext, next):
        """
        Process the request and optionally transform the response.
        :param request: The incoming request object.
        :param next: A function to call the next interceptor or controller action.
        :return: The response after processing.
        """
        res = await next()
        ctx.get_response().set_header("X-Header", "Value")
        ctx.get_response().set_header("X-Header2", "Value2")
        self.logger.info(f"Setting Response Header {ctx.get_response().get_headers()}")
        return res


app.add_global_interceptor(GlobalLogInterceptor)
app.add_global_interceptor(ResHeadersInterceptor)

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Start the application
    app.run()
