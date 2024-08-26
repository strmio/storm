from storm.core.exception import StormException

class NotFoundException(StormException):
    """
    Exception for resources that are not found.

    :param message: Custom error message, defaults to 'Resource not found'
    """
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class UnauthorizedException(StormException):
    """
    Exception for unauthorized access attempts.

    :param message: Custom error message, defaults to 'Unauthorized access'
    """
    def __init__(self, message="Unauthorized access"):
        super().__init__(message, status_code=401)


class BadRequestException(StormException):
    """
    Exception for bad requests.

    :param message: Custom error message, defaults to 'Bad request'
    """
    def __init__(self, message="Bad request"):
        super().__init__(message, status_code=400)
