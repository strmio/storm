from functools import wraps
from storm.common.enums.http_status import HttpStatus
from storm.common.execution_context import execution_context


def HttpCode(status_code: int):
    """
    Decorator to set the HTTP status code for a route handler.

    :param status_code: The HTTP status code to set for the response.
    """
    if isinstance(status_code, HttpStatus):
        status_code = status_code.value

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current request from the execution context
            response = execution_context.get_response()
            response.update_status_code(status_code)

            return await func(*args, **kwargs)

        # Attach the status code to the function for later retrieval
        wrapper._http_status_code = status_code
        return wrapper

    return decorator
