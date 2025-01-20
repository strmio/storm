from storm.common.exceptions.http import BadRequestException
from .pipe import Pipe


class ValidationPipe(Pipe):
    """
    A generic validation pipe that applies a custom validation function to the input.
    """
    def __init__(self, validate_fn, error_message="Validation failed"):
        """
        :param validate_fn: A callable to validate the input. Should return True or raise an exception.
        :param error_message: The error message if validation fails.
        """
        self.validate_fn = validate_fn
        self.error_message = error_message

    async def transform(self, value, metadata=None):
        """
        Validate the input using the provided validation function.
        :param value: The value to validate.
        :param metadata: Optional metadata for additional context.
        :return: The input value if validation passes.
        :raises ValueError: If validation fails.
        """
        if not self.validate_fn(value):
            raise BadRequestException(self.error_message)
        return value
