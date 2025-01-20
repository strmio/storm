from storm.common.exceptions.exception import StormHttpException

class BadRequestException(StormHttpException):
    """
    Exception raised for bad requests.

    :param message: Error message
    """

    def __init__(self, message="Bad request"):
        super().__init__(message, status_code=400, name="BadRequest")


class UnauthorizedException(StormHttpException):
    """
    Exception raised for unauthorized access attempts.

    :param message: Error message
    """

    def __init__(self, message="Unauthorized access"):
        super().__init__(message, status_code=401, name="Unauthorized")


class ForbiddenException(StormHttpException):
    """
    Exception raised when access to a resource is forbidden.

    :param message: Error message
    """

    def __init__(self, message="Forbidden"):
        super().__init__(message, status_code=403, name="Forbidden")


class NotFoundException(StormHttpException):
    """
    Exception raised when a requested resource is not found.

    :param message: Error message
    """

    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404, name="NotFound")


class MethodNotAllowedException(StormHttpException):
    """
    Exception raised when the HTTP method is not allowed for the requested resource.

    :param message: Error message
    """

    def __init__(self, message="Method not allowed"):
        super().__init__(message, status_code=405, name="MethodNotAllowed")


class ConflictException(StormHttpException):
    """
    Exception raised when a request could not be completed due to a conflict.

    :param message: Error message
    """

    def __init__(self, message="Conflict"):
        super().__init__(message, status_code=409, name="Conflict")


class UnsupportedMediaTypeException(StormHttpException):
    """
    Exception raised when the request media type is unsupported.

    :param message: Error message
    """

    def __init__(self, message="Unsupported media type"):
        super().__init__(message, status_code=415, name="UnsupportedMediaType")


class UnprocessableEntityException(StormHttpException):
    """
    Exception raised when the server understands the content type of the request entity, 
    but was unable to process the contained instructions.

    :param message: Error message
    """

    def __init__(self, message="Unprocessable entity"):
        super().__init__(message, status_code=422, name="UnprocessableEntity")


class TooManyRequestsException(StormHttpException):
    """
    Exception raised when the user has sent too many requests in a given amount of time.

    :param message: Error message
    """

    def __init__(self, message="Too many requests"):
        super().__init__(message, status_code=429, name="TooManyRequests")


class InternalServerErrorException(StormHttpException):
    """
    Exception raised for an unexpected internal server error.

    :param message: Error message
    """

    def __init__(self, message="Internal server error"):
        super().__init__(message, status_code=500, name="InternalServerError")


class ServiceUnavailableException(StormHttpException):
    """
    Exception raised when the service is unavailable.

    :param message: Error message
    """

    def __init__(self, message="Service unavailable"):
        super().__init__(message, status_code=503, name="ServiceUnavailable")


class GatewayTimeoutException(StormHttpException):
    """
    Exception raised when the server, while acting as a gateway or proxy, 
    did not receive a timely response from an upstream server.

    :param message: Error message
    """

    def __init__(self, message="Gateway timeout"):
        super().__init__(message, status_code=504, name="GatewayTimeout")
class NotFoundException(StormHttpException):
    """
    Exception raised when a requested resource is not found.

    :param message: Error message
    """

    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)
