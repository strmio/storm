# src/storm/common/exceptions.py

class StormException(Exception):
    """
    Base class for all custom exceptions in the Storm framework.

    :param message: A descriptive error message
    :param status_code: HTTP status code associated with the error
    """
    def __init__(self, message="An error occurred", status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """
        Converts the exception to a dictionary format.

        :return: A dictionary with error message and status code
        """
        return {"error": self.message, "status_code": self.status_code}
