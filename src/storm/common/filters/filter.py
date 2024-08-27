import logging
from storm.common.exceptions import StormException

logger = logging.getLogger(__name__)

class ExceptionFilter:
    """
    A global exception filter that catches exceptions and standardizes the response format.
    """
    @staticmethod
    async def handle_exception(exception, request=None):
        """
        Handles the exception and returns a formatted response.

        :param exception: The caught exception
        :param request: The HTTP request associated with the exception (optional)
        :return: A tuple containing the response dictionary and status code
        """
        if isinstance(exception, StormException):
            response = exception.to_dict()
            status_code = exception.status_code
        else:
            response = {"error": "Internal server error", "status_code": 500}
            status_code = 500
            logger.error(f"Unhandled exception: {exception}")

        return response, status_code
