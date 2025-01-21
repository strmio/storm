from storm.common.exceptions.http import BadRequestException
from storm.common.pipes.pipe import Pipe

class ValidateNonEmptyPipe(Pipe):
    async def transform(self, value, metadata=None):
        if not value or not isinstance(value, str):
            raise BadRequestException("Value must be a non-empty string")
        return value
