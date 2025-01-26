import uuid

from storm.common.exceptions.http import BadRequestException
from .pipe import Pipe


class ParseUUIDPipe(Pipe):
    """
    Pipe to parse and validate a value as a UUID.
    """

    async def transform(self, value, metadata=None):
        """
        Transform the input value into a UUID.
        :param value: The value to transform.
        :param metadata: Optional metadata for additional context.
        :return: A UUID object if the value is valid.
        :raises ValueError: If the value is not a valid UUID.
        """
        try:
            return uuid.UUID(value)
        except ValueError:
            param_name = (
                metadata.get("param_name", "unknown") if metadata else "unknown"
            )
            raise BadRequestException(
                f"Invalid value for parameter '{param_name}': {value}. Expected a valid UUID."
            )
