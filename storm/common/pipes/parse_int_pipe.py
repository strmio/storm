from storm.common.exceptions.http import BadRequestException
from .pipe import Pipe


class ParseIntPipe(Pipe):
    """
    Pipe to parse a value as an integer.
    """

    async def transform(self, value, metadata=None):
        try:
            return int(value)
        except ValueError:
            param_name = metadata.get("param_name", "unknown")
            raise BadRequestException(
                f"Invalid value for parameter '{param_name}': {value}. Expected an integer."
            ) from None
