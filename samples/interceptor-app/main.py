from storm.core import StormApplication
from storm.common import Interceptor, Logger, ExecutionContext
from modules.app_module import AppModule


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
        self.logger.info(f"Logging Request {ctx}")
        res = await next()
        self.logger.info(f"Logging Response {res}")
        return res


app.add_global_interceptor(GlobalLogInterceptor)
# app.add_global_interceptor(GlobalReqInterceptor)

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Start the application
    app.run()
