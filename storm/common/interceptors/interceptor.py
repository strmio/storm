class Interceptor:
    """
    Base class for all interceptors. Interceptors can transform requests before they reach the controller
    and responses after the controller has processed the request.
    """
    async def intercept(self, request, next):
        """
        Process the request and optionally transform the response.
        :param request: The incoming request object.
        :param next: A function to call the next interceptor or controller action.
        :return: The response after processing.
        """
        return await next()
