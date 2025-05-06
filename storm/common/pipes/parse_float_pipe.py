from storm.common.exceptions.http import BadRequestException

from .pipe import Pipe


class ParseFloatPipe(Pipe):
    """
    Pipe to parse and validate a value as a float.
    """

    async def transform(self, value, metadata=None):
        try:
            return float(value)
        except ValueError as e:
            raise BadRequestException(f"Invalid float value: {value}") from e
